from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        'Фото',
        upload_to='users/',
        blank=True
    )
    phone = models.CharField(max_length=12, blank=True)
    is_author = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
