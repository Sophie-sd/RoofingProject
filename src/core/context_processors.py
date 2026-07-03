from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from .data import (
    CALLBACK_HINT,
    LOGO_PATH,
    MATERIAL_BRANDS,
    NAV_ITEMS,
    SITE_CONTACT,
    SITE_HOURS,
    SITE_STATS,
)


def site_context(request):
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

    return {
        'site_name': 'Покрівля під ключ',
        'site_name_line1': 'Покрівля',
        'site_name_line2': 'під ключ',
        'logo_url': f'{static(LOGO_PATH)}?v=8',
        'nav_links': nav_links,
        'estimate_url': reverse('core:home') + '#contact',
        'site_contact': SITE_CONTACT,
        'site_stats': SITE_STATS,
        'site_hours': SITE_HOURS,
        'material_brands': MATERIAL_BRANDS,
        'callback_hint': CALLBACK_HINT,
        'telegram_bot_username': getattr(settings, 'TELEGRAM_BOT_USERNAME', ''),
        'telegram_bot_url': (
            f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}'
            if getattr(settings, 'TELEGRAM_BOT_USERNAME', '')
            else ''
        ),
    }


def _active_key(request, item):
    path = request.path.rstrip('/') or '/'
    contacts_path = reverse('core:contacts').rstrip('/') or '/contacts'

    if item['key'] in ('faq', 'contacts'):
        if path != contacts_path:
            return None
        section = request.GET.get('section', 'faq')
        return item['key'] if section == item['key'] else None

    active_map = {
        '/': 'home',
        '/services': 'services',
        '/portfolio': 'portfolio',
        '/about': 'about',
    }
    return item['key'] if active_map.get(path) == item['key'] else None
