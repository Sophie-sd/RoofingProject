from django.urls import path

from . import views
from . import views_chat

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path(
        'portfolio/<slug:city>/',
        views.PortfolioProjectView.as_view(),
        name='portfolio_project',
    ),
    path('contacts/', views.ContactsFaqView.as_view(), name='contacts'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank_you'),
    path('htmx/estimate/', views.htmx_estimate, name='htmx_estimate'),
    path('htmx/estimate-request/', views.htmx_estimate_request, name='htmx_estimate_request'),
    path('htmx/callback/', views.htmx_callback, name='htmx_callback'),
    path('htmx/portfolio/', views.htmx_portfolio, name='htmx_portfolio'),
    path('htmx/faq/<int:pk>/toggle/', views.htmx_faq_toggle, name='htmx_faq_toggle'),
    path('htmx/mobile-nav/', views.htmx_mobile_nav, name='htmx_mobile_nav'),
    path('htmx/chat/send/', views_chat.htmx_chat_send, name='htmx_chat_send'),
    path('htmx/chat/messages/', views_chat.htmx_chat_messages, name='htmx_chat_messages'),
    path('htmx/chat/reset/', views_chat.htmx_chat_reset, name='htmx_chat_reset'),
    path(
        'telegram/webhook/<str:secret>/',
        views_chat.telegram_webhook,
        name='telegram_webhook',
    ),
]
