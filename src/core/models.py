import secrets
import string

from django.db import models

from .models_content import (  # noqa: F401
    AboutFeature,
    ContentPage,
    FaqItem,
    HomeBlock,
    MarqueeItem,
    PortfolioItem,
    ServiceItem,
    SiteSettings,
    WhyUsItem,
)


def generate_session_key():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))


class TelegramConversation(models.Model):
    session_key = models.CharField(max_length=6, unique=True, db_index=True, default=generate_session_key)
    visitor_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'#{self.session_key}'


class TelegramMessage(models.Model):
    SENDER_VISITOR = 'visitor'
    SENDER_OPERATOR = 'operator'
    SENDER_CHOICES = [
        (SENDER_VISITOR, 'Відвідувач'),
        (SENDER_OPERATOR, 'Оператор'),
    ]

    conversation = models.ForeignKey(
        TelegramConversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    telegram_message_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.text[:40]}'
