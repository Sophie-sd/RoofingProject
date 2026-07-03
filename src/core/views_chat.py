import json
import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import TelegramMessage
from .services.chat import (
    get_messages_for_conversation,
    get_or_create_conversation,
    get_session_key,
    mark_operator_messages_read,
    save_visitor_message,
)
from .services.telegram import send_chat_message_to_operator
from .services.telegram_bot import process_telegram_update

logger = logging.getLogger('core')

MAX_MESSAGE_LENGTH = 2000
MAX_NAME_LENGTH = 100


def _parse_after_id(request):
    raw = request.GET.get('after_id', '0')
    try:
        return max(int(raw), 0)
    except (TypeError, ValueError):
        return 0


def _validate_message(text):
    text = (text or '').strip()
    if not text:
        return '', 'Введіть повідомлення'
    if len(text) > MAX_MESSAGE_LENGTH:
        return '', f'Повідомлення занадто довге (макс. {MAX_MESSAGE_LENGTH} символів)'
    return text, ''


@csrf_exempt
@require_http_methods(['POST'])
def telegram_webhook(request, secret):
    expected_secret = getattr(settings, 'TELEGRAM_WEBHOOK_SECRET', '')
    if not expected_secret or secret != expected_secret:
        return HttpResponse(status=403)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponse(status=400)

    try:
        process_telegram_update(payload)
    except Exception:
        logger.exception('Failed to process Telegram update')

    return JsonResponse({'ok': True})


@require_http_methods(['POST'])
def htmx_chat_send(request):
    visitor_name = (request.POST.get('visitor_name') or '').strip()[:MAX_NAME_LENGTH]
    text, error = _validate_message(request.POST.get('message'))
    conversation = get_or_create_conversation(request, visitor_name=visitor_name)

    if error:
        return render(request, 'htmx/chat_messages.html', {
            'messages': get_messages_for_conversation(conversation),
            'conversation': conversation,
            'error': error,
            'visitor_name': visitor_name or conversation.visitor_name,
            'after_id': conversation.messages.order_by('-id').values_list('id', flat=True).first() or 0,
        })

    message = save_visitor_message(conversation, text)
    telegram_message_id = send_chat_message_to_operator(conversation, text)
    if telegram_message_id:
        message.telegram_message_id = telegram_message_id
        message.save(update_fields=['telegram_message_id'])

    messages = get_messages_for_conversation(conversation)
    last_id = message.id

    return render(request, 'htmx/chat_messages.html', {
        'messages': messages,
        'conversation': conversation,
        'visitor_name': conversation.visitor_name,
        'after_id': last_id,
        'clear_input': True,
    })


@require_http_methods(['GET'])
def htmx_chat_messages(request):
    session_key = get_session_key(request)
    if not session_key:
        return render(request, 'htmx/chat_messages.html', {
            'messages': [],
            'conversation': None,
            'after_id': 0,
        })

    conversation = get_or_create_conversation(request)
    after_id = _parse_after_id(request)
    new_messages = list(get_messages_for_conversation(conversation, after_id=after_id))

    if new_messages:
        operator_ids = [
            msg.id for msg in new_messages
            if msg.sender == TelegramMessage.SENDER_OPERATOR
        ]
        if operator_ids:
            mark_operator_messages_read(conversation, after_id=after_id)

    last_id = new_messages[-1].id if new_messages else after_id

    return render(request, 'htmx/chat_messages.html', {
        'messages': new_messages,
        'conversation': conversation,
        'visitor_name': conversation.visitor_name,
        'after_id': last_id,
        'is_poll': True,
    })
