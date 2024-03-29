# Generated by Django 2.2.16 on 2022-02-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="Заголовок"),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
                ("description", models.TextField(verbose_name="Описание")),
            ],
            options={
                "verbose_name": "Группа",
                "verbose_name_plural": "Группы",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Текст нового поста", verbose_name="Текст"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="posts/", verbose_name="Картинка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "ordering": ["-created"],
            },
        ),
    ]
