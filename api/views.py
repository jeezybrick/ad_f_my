import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from publisher.models import Publisher, Website


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
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = SponsorType.objects.all()

        serializer = serializers.SponsorTypeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class PublisherWebsiteList(generics.GenericAPIView):

    serializer_class = serializers.PublisherWebsiteSerializer
    queryset = Website.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Website.objects.all()

        serializer = serializers.PublisherWebsiteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PublisherWebsiteSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save(commit=False)
            print(test)
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:
            publisher = Publisher.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            publisher = self.request.user

        #serializer.save(publisher=publisher)
