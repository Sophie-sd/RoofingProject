import logging
import re

from ..models import TelegramConversation, TelegramMessage
from .telegram import send_reply_to_user

logger = logging.getLogger('core')

SESSION_KEY_PATTERN = re.compile(r'#([A-Z0-9]{6})')


def extract_session_key(text):
    if not text:
        return ''
    match = SESSION_KEY_PATTERN.search(text)
    return match.group(1) if match else ''


def process_telegram_update(update):
    message = update.get('message') or update.get('edited_message')
    if not message:
        return False

    reply_to = message.get('reply_to_message')
    if not reply_to:
        return False

    session_key = extract_session_key(reply_to.get('text', ''))
    if not session_key:
        return False

    conversation = TelegramConversation.objects.filter(
        session_key=session_key,
        is_active=True,
    ).first()
    if not conversation:
        logger.warning('Conversation not found for session key #%s', session_key)
        return False

    text = (message.get('text') or '').strip()
    if not text:
        return False

    telegram_message_id = message.get('message_id')
    if TelegramMessage.objects.filter(telegram_message_id=telegram_message_id).exists():
        return True

    return send_reply_to_user(
        conversation,
        text,
        telegram_message_id=telegram_message_id,
    )
