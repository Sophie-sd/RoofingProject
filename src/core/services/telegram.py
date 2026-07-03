import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger('core')

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/sendMessage'


def _send_telegram_message(text, reply_to_message_id=None):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    if not token or not chat_id:
        logger.info('Telegram credentials not configured; skipping notification')
        return None

    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id

    data = urllib.parse.urlencode(payload).encode('utf-8')
    url = TELEGRAM_API_URL.format(token=token)
    request = urllib.request.Request(
        url,
        data=data,
        method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = json.loads(response.read().decode('utf-8'))
            if not body.get('ok'):
                logger.error('Telegram API error: %s', body)
                return None
            return body.get('result')
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        logger.error('Failed to send Telegram notification: %s', exc)
        return None


def _choice_label_from_data(field_name, cleaned_data):
    from ..data import AREA_CHOICES, FLOORS_CHOICES, ROOF_MATERIALS, WORK_TYPE_CHOICES

    choices_map = {
        'work_type': WORK_TYPE_CHOICES,
        'area': AREA_CHOICES,
        'floors': FLOORS_CHOICES,
        'material': ROOF_MATERIALS,
    }
    value = cleaned_data.get(field_name, '')
    return dict(choices_map.get(field_name, [])).get(value, value)


def format_estimate_message(cleaned_data, source=''):
    lines = [
        'Нова заявка на кошторис',
        f'Населений пункт: {cleaned_data.get("settlement", "")}',
        f'Тип робіт: {_choice_label_from_data("work_type", cleaned_data)}',
        f'Площа: {_choice_label_from_data("area", cleaned_data)}',
        f'Поверхів: {_choice_label_from_data("floors", cleaned_data)}',
        f'Матеріал: {_choice_label_from_data("material", cleaned_data)}',
        f'Телефон: {cleaned_data.get("phone", "")}',
    ]
    if source:
        lines.append(f'Джерело: {source}')
    return '\n'.join(lines)


def send_lead_notification(cleaned_data, source=''):
    text = format_estimate_message(cleaned_data, source=source)
    return _send_telegram_message(text) is not None


def format_chat_message(session_key, visitor_name, text):
    name = visitor_name or 'Відвідувач'
    return f'💬 Чат #{session_key} | {name}: {text}'


def send_chat_message_to_operator(conversation, text, reply_to_message_id=None):
    message_text = format_chat_message(
        conversation.session_key,
        conversation.visitor_name,
        text,
    )
    result = _send_telegram_message(message_text, reply_to_message_id=reply_to_message_id)
    if not result:
        return None
    return result.get('message_id')


def send_reply_to_user(conversation, text, telegram_message_id=None):
    from .chat import save_operator_message

    save_operator_message(
        conversation,
        text,
        telegram_message_id=telegram_message_id,
    )
    return True
