import os
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangotoolbox.fields import EmbeddedModelField
from adfits.fields import ModelListField
from sponsor.models import Industry
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
    website_logo = models.FileField(_("Upload Logo"), upload_to=get_website_logo_path)
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


class Publisher(models.Model):
    """
    The purpose of the models is to publishers
    """

    name = models.CharField(_("Publisher Name"), max_length=100)
    contact_name = models.CharField(_("Contact Name"), max_length=100)
    address = models.TextField(_("Address"), null=True, blank=True)
    telephone = models.IntegerField(_("Telephone"), max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=75, null=True, blank=True)
    industry = models.ForeignKey(Industry, null=True, blank=True)
    logo = models.FileField(_("Upload Logo"), upload_to=get_publisher_logo_path)
    token = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(_("Note"), null=True, blank=True)
    website = ModelListField(EmbeddedModelField(Website))
    password = models.CharField(max_length=32)
    country = models.ForeignKey(Country, null=True, blank=True)

    class Meta:
        app_label = 'publisher'
        db_table = 'publisher_publisher'

    def __unicode__(self):
        return self.name
