from django.db import models
from django.utils import timezone


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата публикации',
        default=timezone.now
    )

    class Meta:
        abstract = True
