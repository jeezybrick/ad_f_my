from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
from api.utils import is_safe_method


""" check if auth user is author to this item """


class IsPublisherAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if is_safe_method(request) else obj.publisher.myuser_ptr_id == request.user.id
