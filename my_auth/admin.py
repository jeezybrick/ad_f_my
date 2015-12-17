from django.contrib import admin
from my_auth.models import MyUser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", 'is_auth', )

admin.site.register(MyUser, UserAdmin)
