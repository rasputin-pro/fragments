# Generated by Django 2.2.16 on 2022-02-28 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
    ]
