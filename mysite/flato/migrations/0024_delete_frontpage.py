# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-13 20:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flato', '0023_profile_numberofitems'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Frontpage',
        ),
    ]