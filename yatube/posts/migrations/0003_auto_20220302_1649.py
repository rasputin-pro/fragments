# Generated by Django 2.2.16 on 2022-03-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_auto_20220228_1641"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата публикации"
            ),
        ),
    ]
