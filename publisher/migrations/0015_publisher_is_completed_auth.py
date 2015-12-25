# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0014_auto_20151222_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='is_completed_auth',
            field=models.CharField(choices=[(b'advertisers', b'advertisers'), (b'add_website', b'Add website'), (b'get_code', b'Get code')], default=b'advertisers', max_length=100, verbose_name='Complete join network stage'),
        ),
    ]