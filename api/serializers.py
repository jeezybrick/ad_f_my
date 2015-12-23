from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import Country
from publisher.models import Publisher, Website
from sponsor.models import Industry, SponsorType, Sponsor


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)


class SponsorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Sponsor
        fields = ('id', 'name',)

    def to_representation(self, instance):
        pass


class PublisherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    email = serializers.EmailField(read_only=True, required=False)
    sponsor = SponsorSerializer(many=True, required=False, read_only=False)
    count_of_added_websites = serializers.SerializerMethodField(read_only=True)

    def get_count_of_added_websites(self, obj):
        return obj.website.all().count()

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'telephone', 'address', 'country', 'email', 'sponsor', 'count_of_added_websites', )

    def update(self, instance, validated_data):
        sponsors = validated_data.get('sponsor', instance.sponsor)
        for sponsor in sponsors:
            instance.sponsor.add(Sponsor.objects.get(myuser_ptr=sponsor.get('id')))
            instance.save()
        return instance


class SponsorTypeSerializer(serializers.ModelSerializer):
    # sponsor_set = SponsorSerializer(many=True, required=False, read_only=True)
    sponsor_set = serializers.SerializerMethodField()

    def get_sponsor_set(self, obj):
        user = self.context['request'].user
        try:
            publisher = Publisher.objects.get(id=user.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("You're not a publisher!"))
        return obj.sponsor.filter(country=publisher.country)

    class Meta:
        model = SponsorType
        fields = ('id', 'type', 'sponsor_set',)
        read_only_fields = ()


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Industry
        fields = ('id', 'industry_type', 'type')


class PublisherWebsiteSerializer(serializers.ModelSerializer):

    industry = CategorySerializer(many=True, required=False, read_only=False)
    website_logo = serializers.ImageField(allow_empty_file=True)

    class Meta:
        model = Website
        fields = ('id', 'website_name', 'website_domain', 'website_logo', 'industry', 'twitter_name', 'facebook_page',
                  'avg_page_views', 'is_verified', )

    def validate_industry(self, industry):
        return industry

    def create(self, validated_data):
        # Get current publisher
        user = self.context['request'].user
        try:
            publisher = Publisher.objects.get(id=user.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("You're not a publisher!"))
        list_of_categories = validated_data.pop('industry', None)

        website = Website.objects.create(**validated_data)
        website.publishers.add(publisher)
        website.industry.add(*[Industry.objects.get_or_create(id=industry['id'])[0] for industry in list_of_categories])
        website.save()
        return website
