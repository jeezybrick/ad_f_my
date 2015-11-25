import os
from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangotoolbox.fields import EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from adfits.fields import ModelListField
from publisher.models import Publisher, Website
from sponsor.models import Sponsor
from colorful.fields import RGBColorField


ACTION_CHOICES = (
	("vd", "Viewed"), ("cd", "Clicked")
)


def get_campaign_image_path(instance, filename):
	"""
	It would return the image path where campaign 
	images would be stored.
	"""
	
	if instance.token is None:
		token = str(uuid4())
	else:
		token = instance.token
	return os.path.join('campaign', token, filename)		


class Campaign(models.Model):
	"""
	The purpose of the model is to store campaigns.
	"""
	
	campaign_name = models.CharField(_("Campaign Name"), max_length=100)
	sponsor = models.ForeignKey(Sponsor)
	publisher = models.ForeignKey(Publisher)
	website = models.ForeignKey(Website, null=True, blank=True)
	start_date = models.DateField(_("Start Date"))
	end_date = models.DateField(_("End Date"))
	image = models.FileField(_("Image"), upload_to=get_campaign_image_path)
	color = RGBColorField()
	created_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)
	modified_on = models.DateTimeField(null=True, blank=True, auto_now=True)
	token = models.CharField(max_length=100, null=True, blank=True)
	coupons_available = models.IntegerField(_("Coupons Available"), default=0 )
	landing_url = models.URLField(max_length=256, null=True, blank=True)
	objects = MongoDBManager()
	
	class Meta:
		app_label = 'campaign'
		db_table = 'campaign_campaign'

	def __unicode__(self):
	    return self.campaign_name


class Widget(models.Model):
	"""
	This model is used to contain the ads
	"""
	
	widget_name = models.CharField(_("Widget Name"), max_length=100)
	campaign = models.ForeignKey(Campaign)
	embed_code = models.TextField(_("Embedded Code"), null=True, blank=True, default="")
	token = models.CharField(max_length=100, null=True, blank=True,)
	
	class Meta:
		app_label = 'campaign'
		db_table = 'campaign_widget'

	def __unicode__(self):
		return self.widget_name


class CampaignTracker(models.Model):
	widget = models.ForeignKey(Widget)
	campaign = models.ForeignKey(Campaign)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	day = models.IntegerField()
	reference_url = models.CharField(_("Reference Website"), max_length=100)
	reference_token = models.CharField(_("Reference Token"), max_length=100)
	clicked_on = models.DateTimeField()
	action = models.CharField(max_length=4, choices=ACTION_CHOICES)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	website = models.ForeignKey(Website, null=True, blank=True)
	objects = MongoDBManager()

	class Meta:
		app_label = 'campaign'
		db_table = 'campaign_campaigntracker'

	def __unicode__(self):
		return self.widget.widget_name


class EmailNotification(models.Model):
	subject = models.CharField(max_length=256)
	body = models.TextField()
	
	def __unicode__(self):
		return self.subject

