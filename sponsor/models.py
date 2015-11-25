import os
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangotoolbox.fields import EmbeddedModelField


def get_sponsor_logo_path(instance, filename):
	"""
	Defines path for storing logo of the sponsors
	"""
	if instance.token is None:
		token = time.time()
	else:
		token = instance.token
		
	instance.token = token
	return os.path.join('campaign/sponsor_logo/%s/%s') % ( token, filename)


class Industry(models.Model):
	"""
	This model is used for adding industry types of various publishers & sponsors
	"""
	
	industry_type=models.CharField(_("Industry"), max_length=100)

	class Meta:
		app_label = 'campaign'
		db_table = 'campaign_industry'
		verbose_name_plural = "Industries"

	def __unicode__(self):
		return self.industry_type


class Sponsor(models.Model):
	"""
	The purpose of the models is to publishers
	"""

	name = models.CharField(_("Sponsor Name"), max_length=100)
	contact_name = models.CharField(_("Contact Name"), max_length=100)
	address = models.TextField(_("Address"), null=True, blank=True)
	telephone = models.IntegerField(_("Telephone"), max_length=10, null=True, blank=True)
	email = models.EmailField(_("Email"),max_length=75, null=True, blank=True)
	industry = EmbeddedModelField(Industry)
	logo = models.FileField(_("Upload Logo"), upload_to=get_sponsor_logo_path)
	token = models.CharField(max_length=100, null=True, blank=True)
	notes = models.TextField(_("Note"), null=True, blank=True)
	password = models.CharField(max_length = 32)
  
	class Meta:
		app_label = 'sponsor'
		db_table = 'sponsor_sponsor'

	def __unicode__(self):
		return self.name
