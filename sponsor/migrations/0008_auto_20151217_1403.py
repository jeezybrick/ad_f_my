# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 20:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0007_remove_sponsor_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='country',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='telephone',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='type',
        ),
    ]
