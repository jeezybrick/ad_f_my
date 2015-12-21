# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 07:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0010_auto_20151217_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='id',
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='industry',
            field=models.ManyToManyField(blank=True, to='campaign.Industry'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='myuser_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
