from django.utils import timezone

from ..models import TelegramConversation, TelegramMessage


SESSION_KEY_NAME = 'chat_session_key'


def get_session_key(request):
    return request.session.get(SESSION_KEY_NAME, '')


def clear_chat_session(request):
    if SESSION_KEY_NAME in request.session:
        del request.session[SESSION_KEY_NAME]
        request.session.modified = True


def get_or_create_conversation(request, visitor_name=''):
    session_key = get_session_key(request)
    if session_key:
        conversation = TelegramConversation.objects.filter(
            session_key=session_key,
            is_active=True,
        ).first()
        if conversation:
            if visitor_name and not conversation.visitor_name:
                conversation.visitor_name = visitor_name
                conversation.save(update_fields=['visitor_name', 'updated_at'])
            return conversation

    conversation = TelegramConversation.objects.create(
        visitor_name=visitor_name,
    )
    request.session[SESSION_KEY_NAME] = conversation.session_key
    request.session.modified = True
    return conversation


def save_visitor_message(conversation, text):
    message = TelegramMessage.objects.create(
        conversation=conversation,
        sender=TelegramMessage.SENDER_VISITOR,
        text=text,
    )
    conversation.updated_at = timezone.now()
    conversation.save(update_fields=['updated_at'])
    return message


def save_operator_message(conversation, text, telegram_message_id=None):
    message = TelegramMessage.objects.create(
        conversation=conversation,
        sender=TelegramMessage.SENDER_OPERATOR,
        text=text,
        telegram_message_id=telegram_message_id,
        is_read=False,
    )
    conversation.updated_at = timezone.now()
    conversation.save(update_fields=['updated_at'])
    return message


def get_messages_for_conversation(conversation, after_id=0):
    return conversation.messages.filter(id__gt=after_id)


def mark_operator_messages_read(conversation, after_id=0):
    conversation.messages.filter(
        sender=TelegramMessage.SENDER_OPERATOR,
        id__gt=after_id,
        is_read=False,
    ).update(is_read=True)
