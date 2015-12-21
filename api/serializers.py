from rest_framework import serializers
from core.models import Country
from publisher.models import Publisher
from sponsor.models import Industry, SponsorType


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name', )


class PublisherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)


    class Meta:
        model = Publisher
        fields = ('id', 'name', 'telephone', 'address', 'country', 'email', )


class SponsorSerializer(serializers.ModelSerializer):

    sponsor = serializers.SerializerMethodField(read_only=True)

    def get_sponsor(self, obj):
        request = self.context.get('request', None)
        sponsor = False
        if request:
            sponsor = [c.name for c in obj.sponsor_set.filter()]
        return sponsor

    class Meta:
        model = SponsorType
        fields = ('id', 'type', 'sponsor', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Industry
        fields = ('industry_type', )
