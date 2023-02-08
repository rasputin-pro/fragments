from typing import Dict

from django.utils import timezone


def year(request) -> Dict[str, int]:
    """Добавляет переменную с текущим годом."""
    if request:
        return {
            "year": timezone.now().year,
        }
    raise Exception()
