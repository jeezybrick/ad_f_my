import os
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.conf import settings
from publisher.forms import PublisherForm, WebsiteForm
from publisher.models import Publisher, Website
from adfits import constants
from PIL import Image, ImageOps


class PublisherAdmin(admin.ModelAdmin):
    form = PublisherForm
    exclude = ('token', 'password')

    def __init__(self, model, admin_site):
        super(PublisherAdmin, self).__init__(model, admin_site)

    def save_model(self, request, object, form, change):
        """
        The purpose of the method is to perform the post saving action
        """

        object.save()
        object.password = make_password(object.name, salt="adfits")
        token = object.logo.name.split('/')[2]
        object.token = token
        publisher_id = object.id
        size = constants.LOGO_SIZE
        self.ad_logo(publisher_id, size, token)
        object.save()

    def ad_logo(request, publisher_id, size, token):
        """
        The purpose of the method is to get the smaller logo of the publisher
        """

        logo_path = Publisher.objects.get(pk=publisher_id).logo
        name = Publisher.objects.get(pk=publisher_id).name
        im = Image.open(logo_path)
        im = im.resize(constants.LOGO_BOX, Image.ANTIALIAS)
        path_mask = os.path.join(settings.MEDIA_ROOT, "masks/mask.png")
        mask = Image.open(path_mask).convert("L")
        output = ImageOps.fit(im, mask.size, centering=(0, 0))
        output.putalpha(mask)
        name = os.path.join(settings.MEDIA_ROOT, "campaign/publisher_logo",
                            token, "circle.png")
        output.save(name, 'PNG')
        im = output.resize(size, Image.ANTIALIAS)
        im.save(os.path.join(settings.MEDIA_ROOT, "campaign/publisher_logo",
                             token, "publisher_logo.png"))


class WebsiteAdmin(admin.ModelAdmin):
    form = WebsiteForm
    exclude = ('token',)

    def __init__(self, model, admin_site):
        super(WebsiteAdmin, self).__init__(model, admin_site)


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Website, WebsiteAdmin)
