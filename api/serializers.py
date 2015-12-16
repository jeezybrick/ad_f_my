from rest_framework import serializers
from core.models import Country
from publisher.models import Publisher


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name', )


class PublisherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    count_of_websites = serializers.SerializerMethodField('get_count_of_websites')

    def get_count_of_websites(self, obj):
        if obj.website:
            return len(obj.website)
        return False

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'telephone', 'address', 'country', 'email', 'count_of_websites', )
