from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField, ListField
from campaign.models import Campaign, Widget
from publisher.models import Publisher, Website
from sponsor.models import Sponsor
from django_mongodb_engine.contrib import MongoDBManager


class UserToken(models.Model):
	widget = models.ForeignKey(Widget)
	campaign = models.ForeignKey(Campaign)
	website = models.ForeignKey(Website, null=True, blank=True)
	reference_url = models.CharField(max_length=256)
	token = models.CharField(max_length=100)
	day = models.IntegerField(default=0)
	dollar_saved = models.IntegerField(default=0)
	created = models.DateTimeField()
	last_viewed = models.DateField(null=True, blank=True)
	last_saved = models.DateField(null=True, blank=True)
	is_redeemed = models.BooleanField(default=False)
	is_available = models.BooleanField(default=True)
	email = models.EmailField(max_length=100, blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	age = models.IntegerField(default=0, blank=True, null=True)
	sex = models.CharField(max_length=10, blank=True, null=True)
	notify_me = models.NullBooleanField(blank=True, default=False)
	agreed = models.NullBooleanField(blank=True, default=False)
	objects = MongoDBManager()

	def __unicode__(self):
		return self.widget.widget_name


class SaveReward(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget, null=True, blank=True)
	campaign = models.ForeignKey(Campaign, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	coupon_part = models.CharField(max_length=200)
	saved_on = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.widget.widget_name


class RedeemCoupon(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget, null=True, blank=True)
	campaign = models.ForeignKey(Campaign, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	redeem_on = models.DateTimeField()
	objects = MongoDBManager()

	def __unicode__(self):
		return self.usertoken.widget.widget_name


class CouponNotifier(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget, null=True, blank=True)
	campaign = models.ForeignKey(Campaign, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	email = models.EmailField(max_length=254, blank=False, unique=True)
	day = models.IntegerField(default=1)
	date_created = models.DateField(auto_now_add=True)
	website = models.ForeignKey(Website, null=True, blank=True)

	def __unicode__(self):
		return self.email


class CampaignNotifier(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget, null=True, blank=True)
	campaign = models.ForeignKey(Campaign, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	email = models.EmailField(max_length=254, blank=False, unique=True)
	date_created = models.DateField(auto_now_add=True)
	website = models.ForeignKey(Website, null=True, blank=True)
	
	def __unicode__(self):
		return self.email

class Notifications(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget)
	campaign = models.ForeignKey(Campaign)
	publisher = models.ForeignKey(Publisher)
	sponsor = models.ForeignKey(Sponsor)
	email = models.EmailField(max_length=254)
	date_created = models.DateField()
	website = models.ForeignKey(Website)
	notify_type = models.CharField(max_length=20)
	objects = MongoDBManager()
	
	def __unicode__(self):
		return self.email


class SocialShare(models.Model):
	usertoken = models.ForeignKey(UserToken)
	widget = models.ForeignKey(Widget, null=True, blank=True)
	campaign = models.ForeignKey(Campaign, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=True, blank=True)
	sponsor = models.ForeignKey(Sponsor, null=True, blank=True)
	social_type = models.CharField(max_length=20, null=True, blank=True)
	website = models.ForeignKey(Website, null=True, blank=True)
	reference_url = models.CharField(max_length=256)
	date_created = models.DateField()

	def __unicode__(self):
		return self.social_type


class NotificationTracker(models.Model):
	email_reference = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	campaign = models.ForeignKey(Campaign)
	publisher = models.ForeignKey(Publisher)
	sponsor = models.ForeignKey(Sponsor)
	notify_type = models.CharField(max_length=20)
	website = models.ForeignKey(Website)
	sent_status = models.CharField(max_length=20)
	reject_reason = models.TextField()
	day_left = models.IntegerField()
	date_created = models.DateField()

	def __unicode__(self):
		return self.social_type
