# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0008_auto_20151217_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='sponsor',
            field=models.ManyToManyField(blank=True, related_name='sponsor', to='sponsor.Sponsor'),
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='website',
        ),
        migrations.AddField(
            model_name='publisher',
            name='website',
            field=models.ManyToManyField(blank=True, related_name='website', to='publisher.Website'),
        ),
    ]