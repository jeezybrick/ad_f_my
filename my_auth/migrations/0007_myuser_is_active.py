# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0006_remove_myuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
