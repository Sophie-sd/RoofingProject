from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .content_services import (
    get_about_features,
    get_content_page,
    get_faq_items,
    get_home_blocks,
    get_home_portfolio_preview,
    get_marquee_items,
    get_portfolio_city_slugs,
    get_portfolio_filters,
    get_portfolio_items,
    get_service_items,
    get_why_us_items,
    portfolio_city_label,
)
from .forms import CallbackForm, EstimateForm, EstimateRequestForm
from .services.leads import create_estimate_request


def _htmx_redirect_thank_you(request):
    if request.htmx:
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('core:thank_you')
        return response
    return redirect('core:thank_you')


def _page_hero_context(slug):
    page = get_content_page(slug)
    return {
        'hero_image': page.get('header_image_url') or '',
        'hero_eyebrow': page.get('eyebrow', ''),
        'hero_title': page.get('title', ''),
        'hero_lead': page.get('lead', ''),
        'page_body': page.get('body', ''),
    }


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blocks = get_home_blocks()
        hero = blocks['hero']
        context.update({
            'active_nav': 'home',
            'blocks': blocks,
            'hero_image': hero.image_url,
            'estimate_form': EstimateRequestForm(),
            'services_preview': get_service_items(home_only=True),
            'marquee_items': get_marquee_items(),
            'portfolio_preview': get_home_portfolio_preview(),
            'form_title': blocks['cta'].form_title,
            'form_hint': blocks['cta'].form_hint,
        })
        return context


class ServicesView(TemplateView):
    template_name = 'core/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'services',
            **_page_hero_context('services'),
            'services_items': get_service_items(),
            'why_us_items': get_why_us_items(),
            'estimate_form': EstimateRequestForm(),
            'form_source': 'services',
        })
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_block = get_home_blocks().get('about')
        context.update({
            'active_nav': 'about',
            **_page_hero_context('about'),
            'about_block': about_block,
            'about_features': get_about_features(),
            'estimate_form': EstimateRequestForm(),
            'form_source': 'about',
        })
        return context


class PortfolioView(TemplateView):
    template_name = 'core/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', 'all')
        context.update({
            'active_nav': 'portfolio',
            **_page_hero_context('portfolio'),
            'portfolio_items': get_portfolio_items(city),
            'portfolio_filters': get_portfolio_filters(),
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
        city_slugs = get_portfolio_city_slugs()
        if city not in city_slugs:
            raise Http404('Проект не знайдено')

        items = get_portfolio_items(city)
        if not items:
            raise Http404('Проект не знайдено')

        label = portfolio_city_label(city)
        context = super().get_context_data(**kwargs)
        context.update({
            'active_nav': 'portfolio',
            **_page_hero_context('portfolio'),
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
        context.update({
            'active_nav': 'contacts',
            **_page_hero_context('contacts'),
            'faq_items': get_faq_items(open_id=open_id),
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
            **_page_hero_context('privacy'),
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
        create_estimate_request(form.cleaned_data, source=source)
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
    return render(request, 'htmx/portfolio_grid.html', {
        'portfolio_items': get_portfolio_items(city),
        'active_city': city,
        'portfolio_links_enabled': True,
    })


@require_http_methods(['GET'])
def htmx_faq_toggle(request, pk):
    open_id = request.GET.get('open')
    target_id = str(pk)
    new_open = None if open_id == target_id else target_id
    return render(request, 'htmx/faq_list.html', {
        'faq_items': get_faq_items(open_id=new_open),
    })


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
