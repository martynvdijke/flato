# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-15 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flato', '0003_auto_20171214_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_slug',
            field=models.SlugField(default='test', unique=True),
        ),
    ]
