import os
from uuid import uuid4
from django.contrib import admin
from PIL import Image, ImageOps, ImageFilter
from adfits import constants
from django.conf import settings
from campaign.models import Campaign, CampaignTracker, Widget, EmailNotification
from sponsor.models import Industry
from campaign.forms import CampaignForm, WidgetForm


class WidgetAdmin(admin.ModelAdmin):
    readonly_fields = ("embed_code",)
    exclude = ('token',)
    form = WidgetForm

    def __init__(self, model, admin_site):
        super(WidgetAdmin, self).__init__(model, admin_site)

    def save_model(self, request, object, form, change):
        """
        The purpose of this method is to generate embedded script
        for the widget post-saving.
        """
        if object.token is None:
            token = str(uuid4())
        else:
            token = object.token

        object.token = token
        object.save()
        object.embed_code = constants.AD_EMBED_SCRIPT % (token, constants.AD_URL, constants.AD_URL)
        object.save()


class IndustryAdmin(admin.ModelAdmin):
    pass


class EmailNotificationAdmin(admin.ModelAdmin):
    pass


class CampaignAdmin(admin.ModelAdmin):
    # assigning custom campaign form

    exclude = ('token',)

    form = CampaignForm

    class Media:
        js = ['/static/js/custom-admin.js']

    def __init__(self, model, admin_site):
        super(CampaignAdmin, self).__init__(model, admin_site)
'''
    def save_model(self, request, object, form, change):
        """
        The purpose of the method is to perform the post saving action
        """

        object.save()
        token = object.image.name.split('/')[1]
        object.token = token
        campaign_id = object.id
        size = constants.IMG_SIZE
        object.save()
        self.coupons(campaign_id, token, size)

    def coupons(request, campaign_id, token, size):
        """
        The purpose of the method is to get the daily coupons from the image
        """

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "campaign", token)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT, "campaign", token))

        image_file_path = Campaign.objects.get(pk=campaign_id).image
        im = Image.open(image_file_path)
        im = im.resize(size, Image.ANTIALIAS)
        im2 = im.resize(constants.THUMBNAIL_SIZE, Image.ANTIALIAS)
        im2.save(os.path.join(settings.MEDIA_ROOT, "campaign", token, "Thumb.png"))
        im.save(os.path.join(settings.MEDIA_ROOT, "campaign", token, "coupon.png"))
'''

class CampaignTrackerAdmin(admin.ModelAdmin):
    list_display = ('widget', 'campaign', 'reference_url', 'day')
    list_filter = ('action', 'clicked_on')


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(CampaignTracker, CampaignTrackerAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)
