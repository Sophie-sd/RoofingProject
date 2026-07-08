from core.models import FaqItem, PortfolioItem, TelegramConversation


def dashboard_callback(request, context):
    context['dashboard_stats'] = [
        {
            'title': 'FAQ',
            'value': FaqItem.objects.filter(is_active=True).count(),
            'icon': 'help',
            'link': 'admin:core_faqitem_changelist',
        },
        {
            'title': 'Портфоліо',
            'value': PortfolioItem.objects.filter(is_active=True).count(),
            'icon': 'collections',
            'link': 'admin:core_portfolioitem_changelist',
        },
        {
            'title': 'Чати',
            'value': TelegramConversation.objects.filter(is_active=True).count(),
            'icon': 'forum',
            'link': 'admin:core_telegramconversation_changelist',
        },
    ]
    return context
