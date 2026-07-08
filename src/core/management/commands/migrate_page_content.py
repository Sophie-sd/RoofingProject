from django.core.management.base import BaseCommand

from core.content_services import DEFAULT_HOME_BLOCKS
from core.models import (
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
from core.page_content import (
    CONTENT_PAGES,
    DEFAULT_ABOUT_FEATURES,
    DEFAULT_FAQ,
    DEFAULT_HOME_PORTFOLIO,
    DEFAULT_MARQUEE,
    DEFAULT_PORTFOLIO,
    DEFAULT_SERVICES,
    DEFAULT_WHY_US,
    SITE_SETTINGS_DEFAULTS,
    TEXT_FIELD_KEYS,
)


class Command(BaseCommand):
    help = 'Seed CMS defaults into DB (SiteSettings, blocks, pages, lists)'

    def handle(self, *args, **options):
        SiteSettings.objects.update_or_create(pk=1, defaults=SITE_SETTINGS_DEFAULTS)
        self.stdout.write(self.style.SUCCESS('SiteSettings — ok'))

        for key, defaults in DEFAULT_HOME_BLOCKS.items():
            payload = {
                'label': defaults['label'],
                'is_visible': defaults.get('is_visible', True),
            }
            for field in TEXT_FIELD_KEYS:
                if field in defaults:
                    payload[field] = defaults[field]
            HomeBlock.objects.update_or_create(key=key, defaults=payload)
        self.stdout.write(self.style.SUCCESS(f'HomeBlock — {len(DEFAULT_HOME_BLOCKS)}'))

        for slug, source in CONTENT_PAGES.items():
            ContentPage.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': source['title'],
                    'eyebrow': source.get('eyebrow', ''),
                    'lead': source.get('lead', ''),
                    'body': source.get('body', ''),
                    'header_image_url': source.get('header_image_url', ''),
                },
            )
        self.stdout.write(self.style.SUCCESS(f'ContentPage — {len(CONTENT_PAGES)}'))

        if not FaqItem.objects.exists():
            for index, item in enumerate(DEFAULT_FAQ, start=1):
                FaqItem.objects.create(
                    question=item['question'],
                    answer=item['answer'],
                    order=index,
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS(f'FAQ — {len(DEFAULT_FAQ)}'))
        else:
            self.stdout.write('FAQ — skipped')

        if not ServiceItem.objects.exists():
            for index, item in enumerate(DEFAULT_SERVICES, start=1):
                ServiceItem.objects.create(
                    title=item['title'],
                    text=item['text'],
                    icon=item.get('icon', 'roofing'),
                    variant=item.get('variant', 'accent'),
                    features='\n'.join(item.get('features') or []),
                    order=index,
                    is_active=True,
                    show_on_home=True,
                )
            self.stdout.write(self.style.SUCCESS(f'ServiceItem — {len(DEFAULT_SERVICES)}'))
        else:
            self.stdout.write('ServiceItem — skipped')

        if not WhyUsItem.objects.exists():
            for index, item in enumerate(DEFAULT_WHY_US, start=1):
                WhyUsItem.objects.create(
                    num=item.get('num', f'{index:02d}'),
                    title=item['title'],
                    text=item['text'],
                    features='\n'.join(item.get('features') or []),
                    order=index,
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS(f'WhyUsItem — {len(DEFAULT_WHY_US)}'))
        else:
            self.stdout.write('WhyUsItem — skipped')

        if not AboutFeature.objects.exists():
            for index, item in enumerate(DEFAULT_ABOUT_FEATURES, start=1):
                AboutFeature.objects.create(
                    icon=item.get('icon', 'verified'),
                    title=item['title'],
                    text=item['text'],
                    order=index,
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS(f'AboutFeature — {len(DEFAULT_ABOUT_FEATURES)}'))
        else:
            self.stdout.write('AboutFeature — skipped')

        if not MarqueeItem.objects.exists():
            for index, text in enumerate(DEFAULT_MARQUEE, start=1):
                MarqueeItem.objects.create(text=text, order=index, is_active=True)
            self.stdout.write(self.style.SUCCESS(f'MarqueeItem — {len(DEFAULT_MARQUEE)}'))
        else:
            self.stdout.write('MarqueeItem — skipped')

        if not PortfolioItem.objects.exists():
            home_urls = {item['image'] for item in DEFAULT_HOME_PORTFOLIO}
            created = 0
            for index, item in enumerate(DEFAULT_PORTFOLIO, start=1):
                PortfolioItem.objects.create(
                    title=item['title'],
                    city=item['city'],
                    image_url=item['image'],
                    alt=item.get('alt', ''),
                    order=index,
                    is_active=True,
                    show_on_home=item['image'] in home_urls,
                )
                created += 1
            for preview in DEFAULT_HOME_PORTFOLIO:
                exists = PortfolioItem.objects.filter(
                    city=preview['city'],
                    image_url=preview['image'],
                ).exists()
                if not exists:
                    PortfolioItem.objects.create(
                        title=preview['title'],
                        city=preview['city'],
                        image_url=preview['image'],
                        alt=preview.get('alt', ''),
                        order=9000 + created,
                        is_active=True,
                        show_on_home=True,
                    )
                    created += 1
            self.stdout.write(self.style.SUCCESS(f'PortfolioItem — {created}'))
        else:
            self.stdout.write('PortfolioItem — skipped')
