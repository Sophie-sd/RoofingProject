"""Default CMS content — fallback if DB empty / fields blank."""

from .data import (
    ABOUT_FEATURES,
    FAQ_ITEMS,
    HERO_HOME_URL,
    HOME_PORTFOLIO_PREVIEW,
    MARQUEE_ITEMS,
    SERVICES_ITEMS,
    SITE_CONTACT,
    SITE_HOURS,
    SITE_STATS,
    WHY_US_ITEMS,
)
from .portfolio_data import PORTFOLIO_ITEMS

ABOUT_MEDIA_URL = (
    'https://lh3.googleusercontent.com/aida-public/'
    'AB6AXuC8u3vaYUv6ew2u95Q9EniGm6KvMc6ZWpEfCISGTZUQ5RmOMJMfvVYy6tvePa8CuatqzMAwVg02'
    'LQqnjfoZxREU1UcmL1xpSvItqyWX0d9xqYyk6ZJQv917-7QhS066-t1NvaghRhQQA6OORbqMYZrK3ntR9'
    '4QQdqk2flXOJPxXsVqOhbPAwViRqlC_ETmnGsBV_W2OQgob6Rw2wKZRHJG_lHO7FrFhkiKwf5nOrf1nB'
    'LWmjt9epdjFgmpdtZEpiDjMGSsK5-hIZxYC'
)

SITE_SETTINGS_DEFAULTS = {
    'site_name': 'Покрівля під ключ',
    'site_name_line1': 'Покрівля',
    'site_name_line2': 'під ключ',
    'owner': SITE_CONTACT['owner'],
    'location': SITE_CONTACT['location'],
    'phone': SITE_CONTACT['phone'],
    'phone_tel': SITE_CONTACT['phone_tel'],
    'email': SITE_CONTACT['email'],
    'hours_weekdays': SITE_HOURS['weekdays'],
    'hours_weekend': SITE_HOURS['weekend'],
    'stats_projects': SITE_STATS['projects'],
    'stats_experience': SITE_STATS['experience'],
    'stats_warranty': SITE_STATS['warranty_years'],
    'callback_hint': 'Відповімо протягом дня у робочий час',
    'material_brands': 'Ruukki, Braas, Velux, Katepal, BRYZA, RAINWAY',
    'meta_description': (
        'Професійний монтаж покрівлі будь-якої складності. '
        'Скандинавська якість та безкомпромісна надійність.'
    ),
}

DEFAULT_HOME_BLOCKS = {
    'hero': {
        'label': 'Головний банер',
        'is_visible': True,
        'title_line1': 'НАДІЙНА',
        'title_line2': 'ПОКРІВЛЯ.',
        'title_accent': 'ПІД КЛЮЧ.',
        'lead': (
            'Монтаж і реконструкція покрівлі будь-якої складності. '
            'Якісні матеріали від європейських та українських виробників. '
            'Фіксована ціна в договорі.'
        ),
        'cta_text': 'Безкоштовний кошторис',
        'cta_url': '#contact',
        'cta_secondary_text': 'Наші роботи',
        'cta_secondary_url': '#portfolio',
        'image_url': HERO_HOME_URL,
        'stat_1_label': 'Проектів',
        'stat_2_label': 'Років досвіду',
        'stat_3_label': 'Гарантія монтажу',
    },
    'about': {
        'label': 'Про нас (превʼю)',
        'is_visible': True,
        'eyebrow': 'Наша майстерність',
        'heading': 'Майстерність і надійні матеріали',
        'text_1': (
            'Ми не просто будуємо дахи — ми створюємо захисну оболонку вашого дому. '
            'Кожен проект базується на принципах функціональності, довговічності '
            'та візуальної гармонії.'
        ),
        'text_2': (
            'Сертифіковані матеріали {brands} — з офіційною гарантією від виробника.'
        ),
        'checklist': (
            'Якісні матеріали від європейських та українських виробників\n'
            'Гарантія на матеріали від виробника\n'
            'Гарантія до 10 років на монтаж\n'
            'Фіксована ціна без змін у договорі'
        ),
        'link_text': 'Детальніше про нас',
        'link_url': '/about/',
        'image_url': ABOUT_MEDIA_URL,
    },
    'services': {
        'label': 'Послуги (превʼю)',
        'is_visible': True,
        'eyebrow': 'Основні послуги',
        'heading': 'Комплексні рішення для покрівлі',
        'link_text': 'Всі послуги',
        'link_url': '/services/',
    },
    'portfolio': {
        'label': 'Портфоліо (превʼю)',
        'is_visible': True,
        'eyebrow': 'Наші роботи',
        'heading': "Реалізовані об'єкти",
        'link_text': 'Усі проекти',
        'link_url': '/portfolio/',
    },
    'cta': {
        'label': 'Форма зворотного звʼязку',
        'is_visible': True,
        'eyebrow': 'Розрахунок вартості',
        'heading': 'Готові розпочати проект?',
        'lead': (
            'Заповніть форму — ми зателефонуємо протягом дня '
            'і призначимо безкоштовний виїзд для заміру.'
        ),
        'form_title': 'Безкоштовний кошторис',
        'form_hint': 'Відповімо протягом дня у робочий час',
    },
}

TEXT_FIELD_KEYS = (
    'eyebrow',
    'heading',
    'title_line1',
    'title_line2',
    'title_accent',
    'lead',
    'text_1',
    'text_2',
    'checklist',
    'cta_text',
    'cta_url',
    'cta_secondary_text',
    'cta_secondary_url',
    'form_title',
    'form_hint',
    'image_url',
    'link_text',
    'link_url',
    'stat_1_label',
    'stat_2_label',
    'stat_3_label',
)

CONTENT_PAGES = {
    'services': {
        'title': 'Експертні рішення для вашої покрівлі',
        'eyebrow': 'Наші послуги',
        'lead': (
            'Комплексні послуги з монтажу та реконструкції '
            'покрівлі будь-якої складності.'
        ),
        'header_image_url': HERO_HOME_URL,
        'body': '',
    },
    'about': {
        'title': 'Досконалість у кожній лінії',
        'eyebrow': 'Про нас',
        'lead': (
            'Скандинавські стандарти якості, прозорість кошторису '
            'та безкомпромісна надійність у кожному проекті.'
        ),
        'header_image_url': HERO_HOME_URL,
        'body': (
            '<p>Заснована у 2005 році монтажна бригада «покрівля під ключ» '
            'стала провідним гравцем на ринку покрівельних систем Київської області.</p>'
            '<p>Наша місія — забезпечити кожну будівлю дахом, що служить поколінням. '
            'Прозорість кошторису, матеріали найвищого гатунку та суворе дотримання '
            'технологічних карт.</p>'
        ),
    },
    'portfolio': {
        'title': 'Реалізовані проекти',
        'eyebrow': 'Портфоліо',
        'lead': (
            "Кожен об'єкт — поєднання архітектурної точності "
            'та безкомпромісної якості монтажу.'
        ),
        'header_image_url': HERO_HOME_URL,
        'body': '',
    },
    'contacts': {
        'title': 'Ми будуємо не просто дахи, а ваш спокій',
        'eyebrow': 'Питання та контакти',
        'lead': (
            "Зв'яжіться з нами або знайдіть відповіді "
            'на найпоширеніші запитання.'
        ),
        'header_image_url': HERO_HOME_URL,
        'body': '',
    },
    'privacy': {
        'title': 'Політика конфіденційності',
        'eyebrow': 'Правова інформація',
        'lead': 'Останнє оновлення: 1 січня 2024 року',
        'header_image_url': '',
        'body': (
            '<h2>1. Загальні положення</h2>'
            '<p>Монтажна бригада «Покрівля під ключ» поважає вашу конфіденційність '
            'і зобов\'язується захищати персональні дані, які ви надаєте через наш '
            'веб-сайт або під час спілкування з нашими представниками.</p>'
            '<h2>2. Які дані ми збираємо</h2>'
            '<p>Ми можемо збирати ім\'я, номер телефону, адресу електронної пошти '
            'та інформацію про ваш проект покрівлі, яку ви добровільно надаєте '
            'через форми зворотного зв\'язку.</p>'
            '<h2>3. Мета обробки даних</h2>'
            '<p>Ваші дані використовуються виключно для надання консультацій, '
            'підготовки кошторисів, організації виїзду інженера та подальшого '
            'супроводу вашого проекту.</p>'
            '<h2>4. Зберігання та захист</h2>'
            '<p>Ми застосовуємо організаційні та технічні заходи для захисту ваших '
            'даних від несанкціонованого доступу, втрати або розголошення. Дані '
            'зберігаються не довше, ніж це необхідно для досягнення цілей обробки.</p>'
            '<h2>5. Ваші права</h2>'
            '<p>Ви маєте право на доступ, виправлення, видалення своїх персональних '
            'даних, а також право відкликати згоду на їх обробку.</p>'
            '<h2>6. Контакти</h2>'
            '<p>З питань щодо політики конфіденційності звертайтеся за контактами на сайті.</p>'
        ),
    },
}

DEFAULT_FAQ = FAQ_ITEMS
DEFAULT_SERVICES = SERVICES_ITEMS
DEFAULT_WHY_US = WHY_US_ITEMS
DEFAULT_ABOUT_FEATURES = ABOUT_FEATURES
DEFAULT_MARQUEE = MARQUEE_ITEMS
DEFAULT_PORTFOLIO = PORTFOLIO_ITEMS
DEFAULT_HOME_PORTFOLIO = HOME_PORTFOLIO_PREVIEW
