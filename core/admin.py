from django.contrib import admin
from core import models

# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    fields = ("name", )


admin.site.register(models.Country, CountryAdmin)
