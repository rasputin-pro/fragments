# Generated by Django 2.2.16 on 2022-03-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0006_auto_20220302_1709"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата публикации"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата публикации"
            ),
        ),
    ]
