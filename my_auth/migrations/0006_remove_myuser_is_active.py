# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0005_auto_20160105_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_active',
        ),
    ]
