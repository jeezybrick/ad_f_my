import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from publisher.models import Publisher


# Publisher detail
from sponsor.models import Industry


class CurrentPublisherDetail(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.PublisherSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            publisher = Publisher.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            publisher = self.request.user
        return publisher


class CategoryList(APIView):
    def get(self, request):
        parent = request.GET.get('parent', None)
        sub = request.GET.get('sub', None)
        queryset = Industry.objects.all()
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data)
