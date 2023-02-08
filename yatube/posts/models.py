from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(CreatedModel):
    title = models.CharField(
        max_length=120,
        verbose_name="Заголовок",
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст нового поста",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    group = models.ForeignKey(
        "Group",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Слаг",
    )
    description = models.TextField(
        verbose_name="Описание",
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст",
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_follows"
            ),
            # models.CheckConstraint(
            #     check=~models.Q(user=models.F('following')),
            #     name='no_self_follow'
            # )
        ]

    def __str__(self):
        return f"{self.user} -> {self.author}"
