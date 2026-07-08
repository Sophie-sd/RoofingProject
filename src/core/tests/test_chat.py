from django.test import Client, TestCase, override_settings
from django.urls import reverse

from core.models import TelegramConversation, TelegramMessage


class ChatViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_chat_send_creates_conversation_and_message(self):
        response = self.client.post(
            reverse('core:htmx_chat_send'),
            {'visitor_name': 'Іван', 'message': 'Привіт'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TelegramConversation.objects.count(), 1)
        self.assertEqual(TelegramMessage.objects.count(), 1)
        self.assertContains(response, 'Привіт')

    def test_chat_messages_requires_session(self):
        response = self.client.get(reverse('core:htmx_chat_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'chat-message')

    def test_chat_reset_clears_session(self):
        self.client.post(
            reverse('core:htmx_chat_send'),
            {'visitor_name': 'Іван', 'message': 'Привіт'},
        )
        self.assertIn('chat_session_key', self.client.session)
        response = self.client.post(reverse('core:htmx_chat_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('chat_session_key', self.client.session)
        self.assertContains(response, 'id="chat-after-id"')

    @override_settings(TELEGRAM_WEBHOOK_SECRET='test-secret')
    def test_webhook_rejects_invalid_secret(self):
        response = self.client.post(
            reverse('core:telegram_webhook', kwargs={'secret': 'wrong'}),
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    @override_settings(TELEGRAM_WEBHOOK_SECRET='test-secret')
    def test_webhook_accepts_operator_reply(self):
        conversation = TelegramConversation.objects.create(
            session_key='ABC123',
            visitor_name='Іван',
        )
        TelegramMessage.objects.create(
            conversation=conversation,
            sender=TelegramMessage.SENDER_VISITOR,
            text='Питання',
            telegram_message_id=42,
        )
        payload = {
            'message': {
                'message_id': 99,
                'text': 'Відповідь оператора',
                'reply_to_message': {
                    'text': '💬 Чат #ABC123 | Іван: Питання',
                },
            },
        }
        response = self.client.post(
            reverse('core:telegram_webhook', kwargs={'secret': 'test-secret'}),
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TelegramMessage.objects.filter(sender='operator').count(), 1)
