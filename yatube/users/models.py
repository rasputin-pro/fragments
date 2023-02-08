from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField("Фото", upload_to="users/", blank=True)
    about = models.TextField(
        verbose_name="Текст",
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=12, blank=True)
    is_author = models.BooleanField(default=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username
