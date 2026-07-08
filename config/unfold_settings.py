from django.templatetags.static import static
from django.urls import reverse_lazy


def _admin_logo(request):
    return {
        'light': static('images/logo.png'),
        'dark': static('images/logo.png'),
    }


def _favicons(request):
    return [
        {
            'rel': 'icon',
            'sizes': '32x32',
            'type': 'image/png',
            'href': static('images/favicon/favicon-32x32.png'),
        },
        {
            'rel': 'icon',
            'sizes': '16x16',
            'type': 'image/png',
            'href': static('images/favicon/favicon-16x16.png'),
        },
        {
            'rel': 'apple-touch-icon',
            'sizes': '180x180',
            'href': static('images/favicon/apple-touch-icon.png'),
        },
    ]


# Bronze accent from hero text / --color-primary #8c5d28 (hue ~55)
UNFOLD = {
    'SITE_TITLE': 'Покрівля під ключ',
    'SITE_HEADER': 'Покрівля під ключ — Адмінпанель',
    'SITE_SYMBOL': 'roofing',
    'SITE_LOGO': _admin_logo,
    'SITE_FAVICONS': _favicons,
    'SHOW_VIEW_ON_SITE': True,
    'DASHBOARD_CALLBACK': 'core.dashboard.dashboard_callback',
    'COLORS': {
        'primary': {
            '50': 'oklch(97% 0.02 55)',
            '100': 'oklch(94% 0.03 55)',
            '200': 'oklch(88% 0.05 55)',
            '300': 'oklch(78% 0.08 55)',
            '400': 'oklch(68% 0.10 55)',
            '500': 'oklch(58% 0.11 55)',
            '600': 'oklch(50% 0.10 55)',
            '700': 'oklch(42% 0.09 55)',
            '800': 'oklch(35% 0.07 55)',
            '900': 'oklch(28% 0.05 55)',
            '950': 'oklch(20% 0.03 55)',
        },
        'font': {
            'subtle-light': 'oklch(55% 0.01 55)',
            'default-light': 'oklch(22% 0.02 55)',
            'important-light': 'oklch(15% 0.03 55)',
            'subtle-dark': 'oklch(70% 0.01 55)',
            'default-dark': 'oklch(90% 0.01 55)',
            'important-dark': 'oklch(98% 0.005 55)',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'command_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Огляд',
                'items': [
                    {
                        'title': 'Панель',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Налаштування',
                'separator': True,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                ],
            },
            {
                'title': 'Головна',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Блоки головної',
                        'icon': 'dashboard_customize',
                        'link': reverse_lazy('admin:core_homeblock_changelist'),
                    },
                    {
                        'title': 'Стрічка на головній',
                        'icon': 'view_stream',
                        'link': reverse_lazy('admin:core_marqueeitem_changelist'),
                    },
                ],
            },
            {
                'title': 'Сторінки',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Послуги (заголовок)',
                        'icon': 'home_repair_service',
                        'link': '/admin/core/contentpage/?slug=services',
                    },
                    {
                        'title': 'Про нас (заголовок)',
                        'icon': 'info',
                        'link': '/admin/core/contentpage/?slug=about',
                    },
                    {
                        'title': 'Портфоліо (заголовок)',
                        'icon': 'photo_library',
                        'link': '/admin/core/contentpage/?slug=portfolio',
                    },
                    {
                        'title': 'Контакти (заголовок)',
                        'icon': 'contact_page',
                        'link': '/admin/core/contentpage/?slug=contacts',
                    },
                    {
                        'title': 'Політика конфіденційності',
                        'icon': 'policy',
                        'link': '/admin/core/contentpage/?slug=privacy',
                    },
                ],
            },
            {
                'title': 'Контент',
                'separator': True,
                'items': [
                    {
                        'title': 'Послуги (картки)',
                        'icon': 'handyman',
                        'link': reverse_lazy('admin:core_serviceitem_changelist'),
                    },
                    {
                        'title': 'Чому ми',
                        'icon': 'stars',
                        'link': reverse_lazy('admin:core_whyusitem_changelist'),
                    },
                    {
                        'title': 'Фічі «Про нас»',
                        'icon': 'featured_play_list',
                        'link': reverse_lazy('admin:core_aboutfeature_changelist'),
                    },
                    {
                        'title': 'FAQ',
                        'icon': 'help',
                        'link': reverse_lazy('admin:core_faqitem_changelist'),
                    },
                    {
                        'title': 'Портфоліо',
                        'icon': 'collections',
                        'link': reverse_lazy('admin:core_portfolioitem_changelist'),
                    },
                ],
            },
            {
                'title': 'Чат',
                'separator': True,
                'items': [
                    {
                        'title': 'Розмови в чаті',
                        'icon': 'forum',
                        'link': reverse_lazy('admin:core_telegramconversation_changelist'),
                    },
                    {
                        'title': 'Повідомлення чату',
                        'icon': 'chat',
                        'link': reverse_lazy('admin:core_telegrammessage_changelist'),
                    },
                ],
            },
        ],
    },
}

TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'menubar': False,
    'plugins': 'link lists image code',
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link image | code',
    'content_css': False,
    'skin': 'oxide',
    'language': 'uk',
}
