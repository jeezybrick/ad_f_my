from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress
from core.models import TimeStampedModel
from my_auth.managers import CustomUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):

    fullname = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, blank=True)
    is_auth = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username

    def is_authenticated(self):
        return True

    def get_short_name(self):
        "Returns the short name for the user."
        return self.fullname

    def get_full_name(self):
        return self.fullname

'''
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
'''