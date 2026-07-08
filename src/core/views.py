from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .data import (
    ABOUT_FEATURES,
    FAQ_ITEMS,
    HERO_HOME_URL,
    HOME_PORTFOLIO_PREVIEW,
    MARQUEE_ITEMS,
    PORTFOLIO_CITY_SLUGS,
    PORTFOLIO_FILTERS,
    PORTFOLIO_ITEMS,
    SERVICES_ITEMS,
    WHY_US_ITEMS,
    get_portfolio_city_label,
    get_portfolio_items_for_city,
)
from .forms import CallbackForm, EstimateForm, EstimateRequestForm
from .services.telegram import send_lead_notification


def _htmx_redirect_thank_you(request):
    if request.htmx:
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('core:thank_you')
        return response
    return redirect('core:thank_you')


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'home',
            'hero_image': HERO_HOME_URL,
            'estimate_form': EstimateRequestForm(),
            'services_preview': SERVICES_ITEMS,
            'marquee_items': MARQUEE_ITEMS,
            'portfolio_preview': HOME_PORTFOLIO_PREVIEW,
        })
        return context


class ServicesView(TemplateView):
    template_name = 'core/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'services',
            'hero_image': HERO_HOME_URL,
            'hero_eyebrow': 'Наші послуги',
            'hero_title': 'Експертні рішення для вашої покрівлі',
            'hero_lead': (
                'Комплексні послуги з монтажу та реконструкції '
                'покрівлі будь-якої складності.'
            ),
            'services_items': SERVICES_ITEMS,
            'why_us_items': WHY_US_ITEMS,
            'estimate_form': EstimateRequestForm(),
            'form_source': 'services',
        })
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'about',
            'hero_image': HERO_HOME_URL,
            'hero_eyebrow': 'Про нас',
            'hero_title': 'Досконалість у кожній лінії',
            'hero_lead': (
                'Скандинавські стандарти якості, прозорість кошторису '
                'та безкомпромісна надійність у кожному проекті.'
            ),
            'about_features': ABOUT_FEATURES,
            'estimate_form': EstimateRequestForm(),
            'form_source': 'about',
        })
        return context


class PortfolioView(TemplateView):
    template_name = 'core/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', 'all')
        items = PORTFOLIO_ITEMS
        if city != 'all':
            items = [item for item in PORTFOLIO_ITEMS if item['city'] == city]
        context.update({
            'active_nav': 'portfolio',
            'hero_image': HERO_HOME_URL,
            'hero_eyebrow': 'Портфоліо',
            'hero_title': 'Реалізовані проекти',
            'hero_lead': (
                'Кожен об\'єкт — поєднання архітектурної точності '
                'та безкомпромісної якості монтажу.'
            ),
            'portfolio_items': items,
            'portfolio_filters': PORTFOLIO_FILTERS,
            'active_city': city,
            'portfolio_links_enabled': True,
            'estimate_form': EstimateRequestForm(),
            'form_source': 'portfolio',
        })
        return context


class PortfolioProjectView(TemplateView):
    template_name = 'core/portfolio_project.html'

    def get_context_data(self, **kwargs):
        city = kwargs['city']
        if city not in PORTFOLIO_CITY_SLUGS:
            raise Http404('Проект не знайдено')

        items = get_portfolio_items_for_city(city)
        if not items:
            raise Http404('Проект не знайдено')

        label = get_portfolio_city_label(city)
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'portfolio',
            'hero_image': HERO_HOME_URL,
            'hero_eyebrow': 'Портфоліо',
            'hero_title': 'Реалізовані проекти',
            'hero_lead': (
                'Кожен об\'єкт — поєднання архітектурної точності '
                'та безкомпромісної якості монтажу.'
            ),
            'project_city': city,
            'project_title': label,
            'project_images': items,
            'estimate_form': EstimateRequestForm(),
            'form_source': 'portfolio',
        })
        return context


class ContactsFaqView(TemplateView):
    template_name = 'core/contacts_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_id = self.request.GET.get('open')
        faq_items = []
        for item in FAQ_ITEMS:
            faq_items.append({
                **item,
                'is_open': str(item['id']) == open_id if open_id else False,
            })
        context.update({
            'active_nav': 'contacts',
            'hero_image': HERO_HOME_URL,
            'hero_eyebrow': 'Питання та контакти',
            'hero_title': 'Ми будуємо не просто дахи, а ваш спокій',
            'hero_lead': (
                'Зв\'яжіться з нами або знайдіть відповіді '
                'на найпоширеніші запитання.'
            ),
            'faq_items': faq_items,
            'callback_form': CallbackForm(),
            'form_source': 'contacts',
        })
        return context


class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': '',
            'hero_eyebrow': 'Правова інформація',
            'hero_title': 'Політика конфіденційності',
            'hero_lead': 'Останнє оновлення: 1 січня 2024 року',
        })
        return context


class ThankYouView(TemplateView):
    template_name = 'core/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_nav'] = ''
        return context


@require_http_methods(['POST'])
def htmx_estimate(request):
    form = EstimateForm(request.POST)
    if form.is_valid():
        return _htmx_redirect_thank_you(request)
    return render(request, 'htmx/estimate_form.html', {'form': form})


@require_http_methods(['POST'])
def htmx_estimate_request(request):
    form = EstimateRequestForm(request.POST)
    source = request.POST.get('source', 'page')
    if form.is_valid():
        send_lead_notification(form.cleaned_data, source=source)
        return _htmx_redirect_thank_you(request)
    context = {
        'form': form,
        'form_source': source,
    }
    if source == 'home':
        return render(request, 'partials/home_cta_form.html', context)
    return render(request, 'partials/estimate_form.html', context)


@require_http_methods(['POST'])
def htmx_callback(request):
    form = CallbackForm(request.POST)
    source = request.POST.get('source', 'page')
    if form.is_valid():
        return _htmx_redirect_thank_you(request)
    context = {
        'form': form,
        'form_type': 'callback',
        'form_source': source,
        'show_message_field': source == 'contacts',
        'submit_label': 'Надіслати запит' if source == 'contacts' else 'Отримати кошторис безкоштовно',
    }
    return render(request, 'partials/site_form.html', context)


@require_http_methods(['GET'])
def htmx_portfolio(request):
    city = request.GET.get('city', 'all')
    items = PORTFOLIO_ITEMS
    if city != 'all':
        items = [item for item in PORTFOLIO_ITEMS if item['city'] == city]
    return render(request, 'htmx/portfolio_grid.html', {
        'portfolio_items': items,
        'active_city': city,
        'portfolio_links_enabled': True,
    })


@require_http_methods(['GET'])
def htmx_faq_toggle(request, pk):
    open_id = request.GET.get('open')
    target_id = str(pk)
    new_open = None if open_id == target_id else target_id
    faq_items = []
    for item in FAQ_ITEMS:
        faq_items.append({
            **item,
            'is_open': str(item['id']) == new_open if new_open else False,
        })
    return render(request, 'htmx/faq_list.html', {'faq_items': faq_items})


PATH_ACTIVE_NAV = {
    '/': 'home',
    '/services/': 'services',
    '/about/': 'about',
    '/portfolio/': 'portfolio',
    '/contacts/': 'contacts',
}


@require_http_methods(['GET'])
def htmx_mobile_nav(request):
    open_menu = request.GET.get('open') == '1'
    return render(request, 'partials/mobile_nav.html', {
        'mobile_nav_open': open_menu,
        'active_nav': PATH_ACTIVE_NAV.get(request.path, ''),
    })
