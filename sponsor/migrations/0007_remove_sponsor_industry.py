# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0006_auto_20151217_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='industry',
        ),
    ]