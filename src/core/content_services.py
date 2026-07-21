from types import SimpleNamespace

from .models import (
    AboutFeature,
    AnalyticsSettings,
    ContentPage,
    FaqItem,
    HomeBlock,
    MarqueeItem,
    PortfolioItem,
    ServiceItem,
    SiteSettings,
    WhyUsItem,
)
from .page_content import (
    CONTENT_PAGES,
    DEFAULT_ABOUT_FEATURES,
    DEFAULT_FAQ,
    DEFAULT_HOME_BLOCKS,
    DEFAULT_HOME_PORTFOLIO,
    DEFAULT_MARQUEE,
    DEFAULT_PORTFOLIO,
    DEFAULT_SERVICES,
    DEFAULT_WHY_US,
    SITE_SETTINGS_DEFAULTS,
    TEXT_FIELD_KEYS,
)
from .portfolio_data import PORTFOLIO_CITY_SLUGS, PORTFOLIO_FILTERS, get_portfolio_city_label


def _merge_block(block, defaults):
    data = {'key': block.key if block else '', 'is_visible': True}
    source = defaults or {}
    if block is not None:
        data['is_visible'] = block.is_visible
        data['label'] = block.label
        for field in TEXT_FIELD_KEYS:
            value = getattr(block, field, '') or ''
            data[field] = value if value else source.get(field, '')
        data['image_url'] = block.resolved_image_url() or source.get('image_url', '')
        data['checklist_items'] = block.checklist_items() or [
            line.strip()
            for line in (source.get('checklist') or '').splitlines()
            if line.strip()
        ]
    else:
        data.update({field: source.get(field, '') for field in TEXT_FIELD_KEYS})
        data['label'] = source.get('label', '')
        data['is_visible'] = source.get('is_visible', True)
        data['checklist_items'] = [
            line.strip()
            for line in (source.get('checklist') or '').splitlines()
            if line.strip()
        ]
    return SimpleNamespace(**data)


def get_site_settings():
    try:
        obj = SiteSettings.get_solo()
        return obj
    except Exception:
        return SimpleNamespace(**SITE_SETTINGS_DEFAULTS, brands_list=lambda: [])


def get_analytics_settings():
    try:
        return AnalyticsSettings.get_solo()
    except Exception:
        return SimpleNamespace(
            gtm_id='GTM-WCRM2Z4W',
            ads_id='AW-18337015115',
        )


def get_site_contact():
    settings_obj = get_site_settings()
    if hasattr(settings_obj, 'as_contact'):
        return settings_obj.as_contact()
    return {
        'owner': getattr(settings_obj, 'owner', SITE_SETTINGS_DEFAULTS['owner']),
        'location': getattr(settings_obj, 'location', SITE_SETTINGS_DEFAULTS['location']),
        'phone': getattr(settings_obj, 'phone', SITE_SETTINGS_DEFAULTS['phone']),
        'phone_tel': getattr(settings_obj, 'phone_tel', SITE_SETTINGS_DEFAULTS['phone_tel']),
        'email': getattr(settings_obj, 'email', SITE_SETTINGS_DEFAULTS['email']),
    }


def get_site_stats():
    settings_obj = get_site_settings()
    if hasattr(settings_obj, 'as_stats'):
        return settings_obj.as_stats()
    return {
        'projects': SITE_SETTINGS_DEFAULTS['stats_projects'],
        'experience': SITE_SETTINGS_DEFAULTS['stats_experience'],
        'warranty_years': SITE_SETTINGS_DEFAULTS['stats_warranty'],
    }


def get_site_hours():
    settings_obj = get_site_settings()
    if hasattr(settings_obj, 'as_hours'):
        return settings_obj.as_hours()
    return {
        'weekdays': SITE_SETTINGS_DEFAULTS['hours_weekdays'],
        'weekend': SITE_SETTINGS_DEFAULTS['hours_weekend'],
    }


def get_material_brands():
    settings_obj = get_site_settings()
    if hasattr(settings_obj, 'brands_list'):
        brands = settings_obj.brands_list()
        if brands:
            return brands
    return [
        part.strip()
        for part in SITE_SETTINGS_DEFAULTS['material_brands'].split(',')
        if part.strip()
    ]


def get_home_blocks():
    blocks = {}
    try:
        db_map = {item.key: item for item in HomeBlock.objects.all()}
    except Exception:
        db_map = {}

    for key, defaults in DEFAULT_HOME_BLOCKS.items():
        blocks[key] = _merge_block(db_map.get(key), defaults)
        if key == 'about' and '{brands}' in (blocks[key].text_2 or ''):
            brands = ', '.join(get_material_brands())
            blocks[key].text_2 = blocks[key].text_2.format(brands=brands)
    return blocks


def get_content_page(slug):
    fallback = CONTENT_PAGES.get(slug, {})
    try:
        page = ContentPage.objects.get(slug=slug)
        data = page.as_dict()
        for key, value in fallback.items():
            if not data.get(key):
                data[key] = value
        return data
    except ContentPage.DoesNotExist:
        return dict(fallback)
    except Exception:
        return dict(fallback)


def get_faq_items(open_id=None):
    try:
        queryset = FaqItem.objects.filter(is_active=True)
        if queryset.exists():
            items = []
            for item in queryset:
                items.append({
                    'id': item.pk,
                    'question': item.question,
                    'answer': item.answer,
                    'is_open': str(item.pk) == str(open_id) if open_id else False,
                })
            return items
    except Exception:
        pass
    items = []
    for item in DEFAULT_FAQ:
        items.append({
            **item,
            'is_open': str(item['id']) == str(open_id) if open_id else False,
        })
    return items


def get_service_items(home_only=False):
    try:
        queryset = ServiceItem.objects.filter(is_active=True)
        if home_only:
            queryset = queryset.filter(show_on_home=True)
        if queryset.exists():
            return [item.as_dict() for item in queryset]
    except Exception:
        pass
    return list(DEFAULT_SERVICES)


def get_why_us_items():
    try:
        queryset = WhyUsItem.objects.filter(is_active=True)
        if queryset.exists():
            return [item.as_dict() for item in queryset]
    except Exception:
        pass
    return list(DEFAULT_WHY_US)


def get_about_features():
    try:
        queryset = AboutFeature.objects.filter(is_active=True)
        if queryset.exists():
            return [item.as_dict() for item in queryset]
    except Exception:
        pass
    return list(DEFAULT_ABOUT_FEATURES)


def get_marquee_items():
    try:
        queryset = MarqueeItem.objects.filter(is_active=True)
        if queryset.exists():
            return [item.text for item in queryset]
    except Exception:
        pass
    return list(DEFAULT_MARQUEE)


def get_portfolio_items(city='all'):
    try:
        queryset = PortfolioItem.objects.filter(is_active=True)
        if city and city != 'all':
            queryset = queryset.filter(city=city)
        if queryset.exists():
            return [item.as_dict() for item in queryset]
    except Exception:
        pass
    items = list(DEFAULT_PORTFOLIO)
    if city and city != 'all':
        items = [item for item in items if item['city'] == city]
    return items


def get_home_portfolio_preview():
    try:
        queryset = PortfolioItem.objects.filter(is_active=True, show_on_home=True)
        if queryset.exists():
            return [item.as_dict() for item in queryset]
    except Exception:
        pass
    return list(DEFAULT_HOME_PORTFOLIO)


def get_portfolio_filters():
    return PORTFOLIO_FILTERS


def get_portfolio_city_slugs():
    try:
        cities = set(
            PortfolioItem.objects.filter(is_active=True).values_list('city', flat=True),
        )
        if cities:
            return cities
    except Exception:
        pass
    return PORTFOLIO_CITY_SLUGS


def portfolio_city_label(city_slug):
    return get_portfolio_city_label(city_slug)
