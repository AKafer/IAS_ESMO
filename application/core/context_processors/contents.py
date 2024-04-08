
from django.utils import timezone


def year(request):
    """Выводим год в футер."""

    return {"year": timezone.now()}
