from django.contrib import admin
from client.models import UserToken

class UserTokenAdmin(admin.ModelAdmin):
	fields = ('widget', 'campaign', 'reference_url', 'day', 'dollar_saved', 'last_viewed', 'last_saved')
	search_fields = ('day',)

admin.site.register(UserToken, UserTokenAdmin)
