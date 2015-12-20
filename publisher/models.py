import os
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from my_auth.models import MyUser
from sponsor.models import Industry, Sponsor
from core.models import Country


def get_publisher_logo_path(instance, filename):
    """
    Defines path for storing logo of the publishers
    """

    if instance.token is None:
        token = time.time()
    else:
        token = instance.token

    instance.token = token
    return os.path.join('campaign/publisher_logo/%s/%s') % (token, filename)


def get_website_logo_path(instance, filename):
    """
    Defines path for storing logo of the publishers
    """

    if instance.token is None:
        token = time.time()
    else:
        token = instance.token

    instance.token = token
    return os.path.join('campaign/website_logo/%s/%s') % (token, filename)


class Website(models.Model):
    """
    This model is used to assign websites types to publisher
    """

    website_name = models.CharField(_("Website Name"), max_length=100)
    website_domain = models.URLField(_("Website Domain"), max_length=100)
    website_logo = models.FileField(_("Upload Logo"), upload_to=get_website_logo_path, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    twitter_name = models.CharField(max_length=100, null=True, blank=True)
    facebook_page = models.CharField(max_length=100, null=True, blank=True)
    avg_page_views = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'publisher'
        db_table = 'publisher_website'

    def __unicode__(self):
        return self.website_name


class Publisher(MyUser):
    """
    The purpose of the models is to publishers
    """
    address = models.TextField(_("Address"), blank=True)
    city = models.CharField(_("City"), blank=True, max_length=80)
    state = models.CharField(_("State"),  blank=True, max_length=50)
    telephone = models.CharField(_("Telephone"), max_length=15, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    logo = models.ImageField(_("Upload Logo"), upload_to='', blank=True)
    notes = models.TextField(_("Note"), blank=True)
    website = models.ManyToManyField(Website, related_name='website', blank=True)
    sponsor = models.ManyToManyField(Sponsor, related_name='sponsor', blank=True)
    country = models.ForeignKey(Country, null=True, blank=False, related_name='country')

    class Meta:
        app_label = 'publisher'
        db_table = 'publisher_publisher'

    def __unicode__(self):
        return self.name
