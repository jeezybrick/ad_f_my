# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0004_auto_20151223_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_auth',
            field=models.BooleanField(default=True),
        ),
    ]
