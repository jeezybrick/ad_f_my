# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 18:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0002_auto_20151217_1128'),
        ('sponsor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='email',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='password',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='token',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='industry',
            field=models.ManyToManyField(blank=True, to='campaign.Industry'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='myuser_ptr',
            field=models.OneToOneField(auto_created=True, default='', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
