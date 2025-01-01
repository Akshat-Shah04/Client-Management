from django import template
from myapp.models import Billing

register = template.Library()


@register.filter
def get_billing_for_service(billings, service_pk):
    """
    Fetch billing information for a specific service.
    Args:
        billings (QuerySet): QuerySet of Billing objects.
        service_pk (int): Primary key of the service to filter by.

    Returns:
        Billing object or None.
    """
    try:
        return billings.filter(clientService__id=service_pk).first()
    except Billing.DoesNotExist:
        return None
