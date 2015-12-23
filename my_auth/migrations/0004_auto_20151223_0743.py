# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0003_myuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
