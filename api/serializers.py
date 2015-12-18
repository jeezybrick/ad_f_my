from rest_framework import serializers
from core.models import Country
from publisher.models import Publisher
from sponsor.models import Industry


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name', )


class PublisherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)


    class Meta:
        model = Publisher
        fields = ('id', 'name', 'telephone', 'address', 'country', 'email', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Industry
        fields = ('industry_type', )
