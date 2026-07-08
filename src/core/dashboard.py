from core.models import EstimateRequest, FaqItem, PortfolioItem, TelegramConversation


def dashboard_callback(request, context):
    context['dashboard_stats'] = [
        {
            'title': 'Нові заявки',
            'value': EstimateRequest.objects.filter(is_processed=False).count(),
            'icon': 'request_quote',
            'link': 'admin:core_estimaterequest_changelist',
        },
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
