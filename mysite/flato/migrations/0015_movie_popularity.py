# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-19 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flato', '0014_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='popularity',
            field=models.TextField(blank=True, null=True),
        ),
    ]
