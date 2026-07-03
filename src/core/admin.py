from django.conf import settings
from django.contrib import admin

from .models import TelegramConversation, TelegramMessage


@admin.register(TelegramConversation)
class TelegramConversationAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'visitor_name', 'is_active', 'updated_at')
    search_fields = ('session_key', 'visitor_name')
    list_filter = ('is_active',)


@admin.register(TelegramMessage)
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'text_preview', 'is_read', 'created_at')
    list_filter = ('sender', 'is_read')
    search_fields = ('text', 'conversation__session_key')

    @admin.display(description='Текст')
    def text_preview(self, obj):
        return obj.text[:60]
