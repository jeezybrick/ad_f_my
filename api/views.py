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
from sponsor.models import Industry, Sponsor, SponsorType


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
        if parent:
            queryset = Industry.objects.filter(industry_type__contains=parent)
        if sub:
            queryset = Industry.objects.filter(industry_type__contains=sub)

        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class AdvertisersList(APIView):
    def get(self, request):
        queryset = SponsorType.objects.all()

        serializer = serializers.SponsorSerializer(queryset, many=True)
        return Response(serializer.data)