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
    session_key = models.CharField('Код сесії', max_length=6, unique=True, db_index=True, default=generate_session_key)
    visitor_name = models.CharField("Ім'я відвідувача", max_length=100, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'розмову в чаті'
        verbose_name_plural = 'Розмови в чаті'
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
        verbose_name='Розмова',
    )
    sender = models.CharField('Відправник', max_length=20, choices=SENDER_CHOICES)
    text = models.TextField('Текст')
    telegram_message_id = models.BigIntegerField('ID у Telegram', null=True, blank=True, db_index=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = 'повідомлення чату'
        verbose_name_plural = 'Повідомлення чату'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.text[:40]}'
