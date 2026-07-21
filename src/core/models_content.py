from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField('Назва сайту', max_length=128, default='Покрівля під ключ')
    site_name_line1 = models.CharField('Назва (рядок 1)', max_length=64, default='Покрівля')
    site_name_line2 = models.CharField('Назва (рядок 2)', max_length=64, default='під ключ')
    owner = models.CharField('Власник', max_length=64, default='Юра')
    location = models.CharField('Локація', max_length=255, default='Біла Церква, Київська обл.')
    phone = models.CharField('Телефон', max_length=32, default='096 409 66 12')
    phone_tel = models.CharField('Телефон (tel:)', max_length=32, default='+380964096612')
    email = models.EmailField('Email', default='pokrivlia.pid.kliuch@gmail.com')
    hours_weekdays = models.CharField(
        'Години (будні)',
        max_length=128,
        default='Пн – Пт: 08:00 – 20:00',
    )
    hours_weekend = models.CharField(
        'Години (вихідні)',
        max_length=128,
        default='Сб – Нд: 09:00 – 18:00',
    )
    stats_projects = models.CharField('Статистика: проекти', max_length=32, default='400+')
    stats_experience = models.CharField('Статистика: досвід', max_length=32, default='20+')
    stats_warranty = models.CharField('Статистика: гарантія', max_length=32, default='10')
    callback_hint = models.CharField(
        'Підказка форми',
        max_length=255,
        default='Відповімо протягом дня у робочий час',
    )
    material_brands = models.TextField(
        'Бренди матеріалів',
        blank=True,
        default='Ruukki, Braas, Velux, Katepal, BRYZA, RAINWAY',
        help_text='Через кому',
    )
    meta_description = models.TextField(
        'Опис для пошуковиків (SEO)',
        blank=True,
        default=(
            'Професійний монтаж покрівлі будь-якої складності. '
            'Скандинавська якість та безкомпромісна надійність.'
        ),
    )
    facebook_url = models.URLField('Facebook', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    youtube_url = models.URLField('YouTube', blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def brands_list(self):
        raw = (self.material_brands or '').strip()
        if not raw:
            return []
        return [part.strip() for part in raw.split(',') if part.strip()]

    def as_contact(self):
        return {
            'owner': self.owner,
            'location': self.location,
            'phone': self.phone,
            'phone_tel': self.phone_tel,
            'email': self.email,
        }

    def as_stats(self):
        return {
            'projects': self.stats_projects,
            'experience': self.stats_experience,
            'warranty_years': self.stats_warranty,
        }

    def as_hours(self):
        return {
            'weekdays': self.hours_weekdays,
            'weekend': self.hours_weekend,
        }

    def save(self, *args, **kwargs):
        digits = ''.join(c for c in (self.phone or '') if c.isdigit())
        if len(digits) == 10:
            self.phone_tel = f'+38{digits}'
        elif len(digits) == 12 and digits.startswith('380'):
            self.phone_tel = f'+{digits}'
        elif digits.startswith('380') and len(digits) > 10:
            self.phone_tel = f'+{digits}'
        super().save(*args, **kwargs)


class AnalyticsSettings(models.Model):
    gtm_container_id = models.CharField(
        'Google Tag Manager ID',
        max_length=32,
        blank=True,
        default='GTM-WCRM2Z4W',
        help_text='Наприклад GTM-XXXXXXX. Порожнє поле — тег вимкнено.',
    )
    google_ads_id = models.CharField(
        'Google Ads ID (gtag)',
        max_length=32,
        blank=True,
        default='AW-18337015115',
        help_text='Наприклад AW-XXXXXXXXXX. Порожнє поле — тег вимкнено.',
    )

    class Meta:
        verbose_name = 'Аналітика Google'
        verbose_name_plural = 'Аналітика Google'

    def __str__(self):
        return 'Аналітика Google'

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.gtm_container_id = (self.gtm_container_id or '').strip().upper()
        self.google_ads_id = (self.google_ads_id or '').strip().upper()
        super().save(*args, **kwargs)

    @property
    def gtm_id(self):
        value = (self.gtm_container_id or '').strip()
        return value if value.startswith('GTM-') else ''

    @property
    def ads_id(self):
        value = (self.google_ads_id or '').strip()
        return value if value.startswith('AW-') else ''


class HomeBlock(models.Model):
    KEY_HERO = 'hero'
    KEY_ABOUT = 'about'
    KEY_SERVICES = 'services'
    KEY_PORTFOLIO = 'portfolio'
    KEY_CTA = 'cta'
    KEY_CHOICES = [
        (KEY_HERO, 'Головний банер'),
        (KEY_ABOUT, 'Про нас (превʼю)'),
        (KEY_SERVICES, 'Послуги (превʼю)'),
        (KEY_PORTFOLIO, 'Портфоліо (превʼю)'),
        (KEY_CTA, 'Форма зворотного звʼязку'),
    ]

    key = models.SlugField('Ключ', unique=True, choices=KEY_CHOICES)
    label = models.CharField('Назва в адмінці', max_length=64)
    is_visible = models.BooleanField(
        'Показувати на головній',
        default=True,
        help_text='Вимкніть, щоб повністю приховати цей блок на сайті.',
    )
    eyebrow = models.CharField('Підпис над заголовком', max_length=128, blank=True)
    heading = models.CharField('Заголовок', max_length=255, blank=True)
    title_line1 = models.CharField('Заголовок рядок 1', max_length=64, blank=True)
    title_line2 = models.CharField('Заголовок рядок 2', max_length=64, blank=True)
    title_accent = models.CharField('Акцентний рядок', max_length=64, blank=True)
    lead = models.TextField('Лід / опис', blank=True)
    text_1 = models.TextField('Текст 1', blank=True)
    text_2 = models.TextField('Текст 2', blank=True)
    checklist = models.TextField(
        'Чеклист',
        blank=True,
        help_text='Кожен пункт з нового рядка',
    )
    cta_text = models.CharField('Кнопка 1 — текст', max_length=64, blank=True)
    cta_url = models.CharField('Кнопка 1 — посилання', max_length=255, blank=True)
    cta_secondary_text = models.CharField('Кнопка 2 — текст', max_length=64, blank=True)
    cta_secondary_url = models.CharField('Кнопка 2 — посилання', max_length=255, blank=True)
    form_title = models.CharField('Заголовок форми', max_length=128, blank=True)
    form_hint = models.CharField('Підказка форми', max_length=255, blank=True)
    image = models.ImageField(
        'Зображення',
        upload_to='blocks/',
        blank=True,
        help_text='Hero / about media. Рекомендовано JPG/WebP до 2 МБ',
    )
    image_url = models.CharField(
        'URL зображення (якщо без upload)',
        max_length=512,
        blank=True,
        help_text='Наприклад /static/images/hero_roof_premium.png',
    )
    link_text = models.CharField('Текст посилання', max_length=64, blank=True)
    link_url = models.CharField('URL посилання', max_length=255, blank=True)
    stat_1_label = models.CharField('Стат 1 — підпис', max_length=64, blank=True)
    stat_2_label = models.CharField('Стат 2 — підпис', max_length=64, blank=True)
    stat_3_label = models.CharField('Стат 3 — підпис', max_length=64, blank=True)

    class Meta:
        verbose_name = 'Блок головної'
        verbose_name_plural = 'Блоки головної'
        ordering = ['key']

    def __str__(self):
        return self.label

    def checklist_items(self):
        raw = (self.checklist or '').strip()
        if not raw:
            return []
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def resolved_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ''


class ContentPage(models.Model):
    slug = models.SlugField('Код сторінки', unique=True)
    title = models.CharField('Заголовок', max_length=255)
    eyebrow = models.CharField('Підпис над заголовком', max_length=128, blank=True)
    lead = models.TextField('Короткий опис', blank=True)
    body = models.TextField('Текст сторінки', blank=True)
    header_image = models.ImageField(
        'Зображення заголовку',
        upload_to='pages/',
        blank=True,
    )
    header_image_url = models.CharField(
        'URL зображення (fallback)',
        max_length=512,
        blank=True,
    )

    class Meta:
        verbose_name = 'Сторінка контенту'
        verbose_name_plural = 'Сторінки контенту'
        ordering = ['slug']

    def __str__(self):
        return self.title

    def resolved_header_image(self):
        if self.header_image:
            return self.header_image.url
        return self.header_image_url or ''

    def as_dict(self):
        return {
            'title': self.title,
            'eyebrow': self.eyebrow,
            'lead': self.lead,
            'body': self.body,
            'header_image_url': self.resolved_header_image(),
        }


class FaqItem(models.Model):
    question = models.CharField('Питання', max_length=255)
    answer = models.TextField('Відповідь')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.question


class ServiceItem(models.Model):
    VARIANT_ACCENT = 'accent'
    VARIANT_DARK = 'dark'
    VARIANT_CHOICES = [
        (VARIANT_ACCENT, 'Акцент'),
        (VARIANT_DARK, 'Темний'),
    ]

    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Опис')
    icon = models.CharField('Іконка (Material Symbol)', max_length=64, default='roofing')
    variant = models.CharField(
        'Варіант',
        max_length=16,
        choices=VARIANT_CHOICES,
        default=VARIANT_ACCENT,
    )
    features = models.TextField(
        'Особливості',
        blank=True,
        help_text='Кожна з нового рядка',
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)
    show_on_home = models.BooleanField('На головній', default=True)

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title

    def features_list(self):
        raw = (self.features or '').strip()
        if not raw:
            return []
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def as_dict(self):
        return {
            'icon': self.icon,
            'variant': self.variant,
            'title': self.title,
            'text': self.text,
            'features': self.features_list(),
        }


class WhyUsItem(models.Model):
    num = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Опис')
    features = models.TextField(
        'Особливості',
        blank=True,
        help_text='Кожна з нового рядка',
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Чому ми'
        verbose_name_plural = 'Чому ми'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title

    def features_list(self):
        raw = (self.features or '').strip()
        if not raw:
            return []
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def as_dict(self):
        return {
            'num': self.num,
            'title': self.title,
            'text': self.text,
            'features': self.features_list(),
        }


class AboutFeature(models.Model):
    icon = models.CharField('Іконка', max_length=64, default='verified')
    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Опис')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Фіча «Про нас»'
        verbose_name_plural = 'Фічі «Про нас»'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'icon': self.icon,
            'title': self.title,
            'text': self.text,
        }


class PortfolioItem(models.Model):
    title = models.CharField('Назва', max_length=128)
    city = models.SlugField('Місто (slug)', max_length=64)
    image = models.ImageField('Фото (upload)', upload_to='portfolio/', blank=True)
    image_url = models.CharField(
        'URL фото',
        max_length=512,
        blank=True,
        help_text='Fallback, якщо немає upload',
    )
    alt = models.CharField('Alt', max_length=255, blank=True)
    date = models.CharField('Дата', max_length=64, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)
    show_on_home = models.BooleanField('На головній', default=False)

    class Meta:
        verbose_name = 'Робота портфоліо'
        verbose_name_plural = 'Портфоліо'
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.title} ({self.city})'

    def resolved_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    def as_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'city': self.city,
            'image': self.resolved_image(),
            'alt': self.alt or self.title,
            'date': self.date,
        }


class MarqueeItem(models.Model):
    text = models.CharField('Текст', max_length=128)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Елемент стрічки'
        verbose_name_plural = 'Стрічка на головній'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.text
