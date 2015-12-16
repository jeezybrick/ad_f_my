import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from publisher.models import Publisher


# Publisher detail
class CurrentPublisherDetail(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.PublisherSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        try:
            queryset = Publisher.objects.get(id=self.request.session['_id'])
        except KeyError:
            queryset = None
        return queryset
