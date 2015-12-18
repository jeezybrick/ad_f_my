import os
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Country
from my_auth.models import MyUser


def get_sponsor_logo_path(instance, filename):
    """
    Defines path for storing logo of the sponsors
    """
    if instance.token is None:
        token = time.time()
    else:
        token = instance.token

    instance.token = token
    return os.path.join('campaign/sponsor_logo/%s/%s') % (token, filename)


class Industry(models.Model):
    """
    This model is used for adding industry types of various publishers & sponsors
    """

    industry_type = models.CharField(_("Industry"), max_length=100)

    class Meta:
        app_label = 'campaign'
        db_table = 'campaign_industry'
        verbose_name_plural = "Industries"

    def __unicode__(self):
        return self.industry_type


class SponsorType(models.Model):
    """
    The purpose of the models is to publishers
    """

    type = models.CharField(_("Sponsor Type"), max_length=100)

    class Meta:
        app_label = 'sponsor'
        db_table = 'sponsor_type'

    def __unicode__(self):
        return self.type


class Sponsor(MyUser):
    """
    The purpose of the models is to publishers
    """

    address = models.TextField(_("Address"), blank=True)
    telephone = models.CharField(_("Telephone"), max_length=20, blank=True)
    industry = models.ManyToManyField(Industry, blank=True)
    logo = models.ImageField(_("Upload Logo"), upload_to='', blank=True)
    notes = models.TextField(_("Note"), blank=True)
    country = models.ForeignKey(Country, blank=False, null=True)
    type = models.ForeignKey(SponsorType, blank=False, null=True)

    class Meta:
        app_label = 'sponsor'
        db_table = 'sponsor_sponsor'

    def __unicode__(self):
        return self.name
