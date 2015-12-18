import os
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.conf import settings
from sponsor.forms import SponsorForm
from sponsor.models import Sponsor, SponsorType
from adfits import constants
from PIL import Image, ImageOps


class SponsorAdmin(admin.ModelAdmin):

    fields = ("email", "name", "logo", "country", "type", )
'''
    form = SponsorForm
    exclude = ('token', 'password')

    def __init__(self, model, admin_site):
        super(SponsorAdmin, self).__init__(model, admin_site)

    def save_model(self, request, object, form, change):
        """
        The purpose of the method is to perform the post saving action
        """

        object.save()
        object.password = make_password(object.name, salt="adfits")
        token = object.logo.name.split('/')[2]
        object.token = token
        sponsor_id = object.id
        size = constants.LOGO_SIZE
        self.ad_logo(sponsor_id, size, token)
        object.save()

    def ad_logo(request, sponsor_id, size, token):
        """
        The purpose of the method is to get the smaller logo of the sponsor
        """

        logo_path = Sponsor.objects.get(pk=sponsor_id).logo
        name = Sponsor.objects.get(pk=sponsor_id).name
        im = Image.open(logo_path)
        im = im.resize(constants.LOGO_BOX, Image.ANTIALIAS)
        path_mask = os.path.join(settings.MEDIA_ROOT, "masks/mask.png")
        mask = Image.open(path_mask).convert("L")
        output = ImageOps.fit(im, mask.size, centering=(0, 0))
        output.putalpha(mask)
        name = os.path.join(settings.MEDIA_ROOT, "campaign/sponsor_logo", token, "circle.png")
        output.save(name, 'PNG')
        im = output.resize(size, Image.ANTIALIAS)
        im.save(os.path.join(settings.MEDIA_ROOT, "campaign/sponsor_logo", token, "sponsor_logo.png"))

'''


class SponsorTypeAdmin(admin.ModelAdmin):
    fields = ("type", )


admin.site.register(SponsorType, SponsorTypeAdmin)

admin.site.register(Sponsor, SponsorAdmin)
