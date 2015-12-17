# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0006_auto_20151217_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='address',
            field=models.TextField(blank=True, default='', verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publisher',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Note'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publisher',
            name='sponsor',
            field=models.ManyToManyField(blank=True, null=True, related_name='sponsor', to='sponsor.Sponsor'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='telephone',
            field=models.CharField(blank=True, default='', max_length=15, verbose_name='Telephone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='website', to='publisher.Website'),
        ),
    ]
