from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from .content_services import (
    get_material_brands,
    get_site_contact,
    get_site_hours,
    get_site_settings,
    get_site_stats,
)
from .data import LOGO_PATH, NAV_ITEMS


def site_context(request):
    settings_obj = get_site_settings()
    nav_links = []
    for item in NAV_ITEMS:
        href = reverse(item['url_name'])
        if item.get('anchor'):
            href = f'{href}#{item["anchor"]}'
        nav_links.append({
            **item,
            'href': href,
            'is_active': item['key'] == _active_key(request, item),
        })

    site_name = getattr(settings_obj, 'site_name', None) or 'Покрівля під ключ'
    return {
        'site_name': site_name,
        'site_name_line1': getattr(settings_obj, 'site_name_line1', None) or 'Покрівля',
        'site_name_line2': getattr(settings_obj, 'site_name_line2', None) or 'під ключ',
        'logo_url': f'{static(LOGO_PATH)}?v=8',
        'nav_links': nav_links,
        'estimate_url': reverse('core:home') + '#contact',
        'site_contact': get_site_contact(),
        'site_stats': get_site_stats(),
        'site_hours': get_site_hours(),
        'material_brands': get_material_brands(),
        'callback_hint': getattr(settings_obj, 'callback_hint', None) or (
            'Відповімо протягом дня у робочий час'
        ),
        'meta_description': getattr(settings_obj, 'meta_description', None) or '',
        'telegram_bot_username': getattr(settings, 'TELEGRAM_BOT_USERNAME', ''),
        'telegram_bot_url': (
            f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}'
            if getattr(settings, 'TELEGRAM_BOT_USERNAME', '')
            else ''
        ),
    }


def _active_key(request, item):
    path = request.path.rstrip('/') or '/'
    if item['key'] == 'home':
        return path == '/'
    if item['key'] in {'faq', 'contacts'}:
        return path.startswith('/contacts')
    target = reverse(item['url_name']).rstrip('/') or '/'
    return path == target or path.startswith(target + '/')
