from ..models import EstimateRequest
from .telegram import send_lead_notification


def create_estimate_request(cleaned_data, source=''):
    """Save estimate lead to DB, then notify Telegram (Telegram failure does not roll back)."""
    request_obj = EstimateRequest.objects.create(
        settlement=cleaned_data['settlement'],
        work_type=cleaned_data['work_type'],
        area=cleaned_data['area'],
        floors=cleaned_data['floors'],
        material=cleaned_data['material'],
        phone=cleaned_data['phone'],
        source=source or '',
    )
    send_lead_notification(cleaned_data, source=source)
    return request_obj
