from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin

from core.admin_forms import ContentPageAdminForm, HomeBlockAdminForm

from .models import (
    AboutFeature,
    ContentPage,
    FaqItem,
    HomeBlock,
    MarqueeItem,
    PortfolioItem,
    ServiceItem,
    SiteSettings,
    TelegramConversation,
    TelegramMessage,
    WhyUsItem,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Бренд', {
            'fields': ('site_name', 'site_name_line1', 'site_name_line2'),
        }),
        ('Контакти', {
            'fields': ('phone', 'email', 'location'),
            'description': (
                'Змінений номер телефону автоматично оновить '
                'посилання для дзвінка (tel:) на сайті.'
            ),
        }),
        ('Години роботи', {
            'fields': ('hours_weekdays', 'hours_weekend', 'callback_hint'),
        }),
        ('Статистика', {
            'fields': ('stats_projects', 'stats_experience', 'stats_warranty'),
        }),
        ('Бренди / SEO', {
            'fields': ('material_brands', 'meta_description'),
        }),
        ('Соцмережі', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url'),
        }),
    )

    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk]),
        )


@admin.register(HomeBlock)
class HomeBlockAdmin(ModelAdmin):
    form = HomeBlockAdminForm
    list_display = ('label', 'is_visible', 'heading_preview')
    list_editable = ('is_visible',)
    list_filter = ('key', 'is_visible')
    search_fields = ('label', 'heading', 'eyebrow')
    readonly_fields = ('key', 'label', 'image_preview')
    ordering = ('key',)

    def get_fieldsets(self, request, obj=None):
        visibility = ('Відображення на сайті', {
            'fields': ('is_visible',),
            'description': 'Вимкніть, щоб приховати блок на головній.',
        })
        if not obj:
            return [visibility]

        if obj.key == HomeBlock.KEY_HERO:
            return [
                visibility,
                ('Заголовок', {
                    'fields': ('title_line1', 'title_line2', 'title_accent', 'lead'),
                }),
                ('Кнопки', {
                    'fields': (
                        'cta_text', 'cta_url',
                        'cta_secondary_text', 'cta_secondary_url',
                    ),
                }),
                ('Підписи статистики', {
                    'fields': ('stat_1_label', 'stat_2_label', 'stat_3_label'),
                }),
                ('Фон', {
                    'fields': ('image', 'image_preview', 'image_url'),
                }),
            ]

        if obj.key == HomeBlock.KEY_ABOUT:
            return [
                visibility,
                ('Тексти', {
                    'fields': ('eyebrow', 'heading', 'text_1', 'text_2', 'checklist'),
                }),
                ('Посилання', {
                    'fields': ('link_text', 'link_url'),
                }),
                ('Фото', {
                    'fields': ('image', 'image_preview', 'image_url'),
                }),
            ]

        if obj.key in {HomeBlock.KEY_SERVICES, HomeBlock.KEY_PORTFOLIO}:
            return [
                visibility,
                ('Тексти', {
                    'fields': ('eyebrow', 'heading', 'link_text', 'link_url'),
                }),
            ]

        if obj.key == HomeBlock.KEY_CTA:
            return [
                visibility,
                ('Тексти', {
                    'fields': ('eyebrow', 'heading', 'lead', 'form_title', 'form_hint'),
                }),
            ]

        return [visibility]

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.display(description='Заголовок')
    def heading_preview(self, obj):
        return obj.heading or obj.title_line1 or '—'

    @admin.display(description='Превʼю')
    def image_preview(self, obj):
        url = obj.resolved_image_url()
        if url:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;object-fit:cover">',
                url,
            )
        return '—'


@admin.register(ContentPage)
class ContentPageAdmin(ModelAdmin):
    form = ContentPageAdminForm
    list_display = ('title', 'slug', 'eyebrow')
    search_fields = ('title', 'slug', 'lead')
    readonly_fields = ('slug', 'header_preview')
    fieldsets = (
        ('Заголовок сторінки', {
            'fields': ('slug', 'eyebrow', 'title', 'lead'),
        }),
        ('Контент', {
            'fields': ('body',),
        }),
        ('Зображення', {
            'fields': ('header_image', 'header_preview', 'header_image_url'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        slug = request.GET.get('slug')
        if slug:
            try:
                obj = ContentPage.objects.get(slug=slug)
            except ContentPage.DoesNotExist:
                obj = None
            if obj:
                return HttpResponseRedirect(
                    reverse('admin:core_contentpage_change', args=[obj.pk]),
                )
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description='Превʼю')
    def header_preview(self, obj):
        url = obj.resolved_header_image()
        if url:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;object-fit:cover">',
                url,
            )
        return '—'


@admin.register(FaqItem)
class FaqItemAdmin(ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    ordering = ('order', 'pk')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'answer':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(ServiceItem)
class ServiceItemAdmin(ModelAdmin):
    list_display = ('title', 'variant', 'order', 'show_on_home', 'is_active')
    list_editable = ('order', 'show_on_home', 'is_active')
    list_filter = ('variant', 'is_active', 'show_on_home')
    search_fields = ('title', 'text')
    ordering = ('order', 'pk')


@admin.register(WhyUsItem)
class WhyUsItemAdmin(ModelAdmin):
    list_display = ('num', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'text')
    ordering = ('order', 'pk')


@admin.register(AboutFeature)
class AboutFeatureAdmin(ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'text')
    ordering = ('order', 'pk')


@admin.register(PortfolioItem)
class PortfolioItemAdmin(ModelAdmin):
    list_display = ('title', 'city', 'image_preview', 'order', 'show_on_home', 'is_active')
    list_editable = ('order', 'show_on_home', 'is_active')
    list_filter = ('city', 'is_active', 'show_on_home')
    search_fields = ('title', 'city', 'alt')
    ordering = ('order', 'pk')
    readonly_fields = ('image_preview',)
    fieldsets = (
        (None, {
            'fields': ('title', 'city', 'alt', 'date'),
        }),
        ('Зображення', {
            'fields': ('image', 'image_preview', 'image_url'),
        }),
        ('Відображення', {
            'fields': ('order', 'show_on_home', 'is_active'),
        }),
    )

    @admin.display(description='Превʼю')
    def image_preview(self, obj):
        url = obj.resolved_image()
        if url:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;object-fit:cover">',
                url,
            )
        return '—'


@admin.register(MarqueeItem)
class MarqueeItemAdmin(ModelAdmin):
    list_display = ('text', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)
    ordering = ('order', 'pk')


@admin.register(TelegramConversation)
class TelegramConversationAdmin(ModelAdmin):
    list_display = ('session_key', 'visitor_name', 'is_active', 'updated_at')
    search_fields = ('session_key', 'visitor_name')
    list_filter = ('is_active',)
    list_display_links = ('session_key',)


@admin.register(TelegramMessage)
class TelegramMessageAdmin(ModelAdmin):
    list_display = ('conversation', 'sender', 'text_preview', 'is_read', 'created_at')
    list_filter = ('sender', 'is_read')
    search_fields = ('text', 'conversation__session_key')

    @admin.display(description='Текст')
    def text_preview(self, obj):
        return obj.text[:60]
