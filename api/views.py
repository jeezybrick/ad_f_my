from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status, permissions, serializers as ser
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from api.permissions import IsAuthorOrReadOnly
from publisher.models import Publisher, Website


# Publisher detail
from sponsor.models import Industry, Sponsor, SponsorType


class CurrentPublisherDetail(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.PublisherSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        try:
            publisher = Publisher.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
             raise ser.ValidationError(_("You're not a publisher!"))
        return publisher

    def get_queryset(self):
        pass


class CategoryList(APIView):
    def get(self, request):
        parent = request.GET.get('parent', None)
        sub = request.GET.get('sub', None)
        if parent:
            lol = Q(industry_type__contains=parent, type='default')
        elif sub:
            lol = Q(industry_type__contains=sub, type='sub')
        else:
            lol = Q()
        queryset = Industry.objects.filter(lol)

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
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = self.get_queryset()

        serializer = serializers.PublisherWebsiteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = serializers.PublisherWebsiteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        try:
            publisher = Publisher.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            raise PermissionDenied("You're not a publisher!")
        queryset = Website.objects.filter(publishers__id__exact=publisher.id)
        return queryset

    def perform_create(self, serializer):
        try:
            publisher = Publisher.objects.get(id=self.request.user.id)
        except ObjectDoesNotExist:
            raise ser.ValidationError(_("You're not a publisher!"))

        serializer.save(publishers=publisher)


class PublisherWebsiteDetail(generics.RetrieveAPIView, generics.UpdateAPIView,):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = serializers.PublisherWebsiteSerializer
    # parser_classes = (FileUploadParser, MultiPartParser, )

    def get_object(self):

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(Website, id=filter_kwargs['pk'])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)

        return obj
