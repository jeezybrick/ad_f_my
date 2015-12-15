# -*- coding: utf-8 -*-

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'core'
        db_table = 'core_country'

    def __unicode__(self):
        return self.name
