from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg, Max, Min, Count, Sum
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


class PublisherSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    email = serializers.EmailField(read_only=True, required=False)
    sponsor = SponsorSerializer(many=True, required=False, read_only=False)
    count_of_added_websites = serializers.SerializerMethodField(read_only=True)
    total_avg_monthly_pageviews = serializers.SerializerMethodField(read_only=True)

    def get_count_of_added_websites(self, obj):
        return obj.websites.all().count()

    def get_total_avg_monthly_pageviews(self, obj):
        return obj.websites.all().aggregate(Sum('avg_page_views')).get('avg_page_views__sum', False)

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'telephone', 'address', 'country', 'email', 'sponsor', 'count_of_added_websites',
                  'total_avg_monthly_pageviews', 'is_completed_auth', )
        read_only_fields = ('is_completed_auth', )

    def update(self, instance, validated_data):
        sponsors = validated_data.get('sponsor', instance.sponsor)
        instance.name = validated_data.get('name', instance.name)
        instance.telephone = validated_data.get('telephone', instance.telephone)

        for sponsor in sponsors:
            instance.sponsor.add(Sponsor.objects.get(id=sponsor.get('id')))
            instance.save()

        if instance.is_completed_auth != 'completed':
            instance.is_completed_auth = 'add_website'

        instance.save()
        return instance


class SponsorTypeSerializer(serializers.ModelSerializer):
    sponsor_set = serializers.SerializerMethodField()

    def get_sponsor_set(self, obj):
        user = self.context['request'].user
        try:
            publisher = Publisher.objects.get(id=user.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("You're not a publisher!"))

        queryset = obj.sponsor_set.filter(country=publisher.country)
        serializer = SponsorSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = SponsorType
        fields = ('id', 'type', 'sponsor_set',)
        read_only_fields = ()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Industry
        fields = ('industry_type', 'type')


class PublisherWebsiteSerializer(serializers.ModelSerializer):
    industry = CategorySerializer(many=True, required=False, read_only=True)
    website_logo = serializers.ImageField(allow_empty_file=True, required=False, read_only=False)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = Website
        fields = ('id', 'website_name', 'website_domain', 'website_logo', 'industry', 'twitter_name', 'facebook_page',
                  'avg_page_views', 'is_verified',)

    def validate_industry(self, industry):
        return industry

    def create(self, validated_data):
        # Get current publisher
        user = self.context['request'].user
        try:
            publisher = Publisher.objects.get(id=user.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("You're not a publisher!"))

        list_of_categories = self.context['request'].data.pop('industry', None)

        if isinstance(list_of_categories, list):
            list_of_categories = list_of_categories[0]

        website = Website.objects.create(**validated_data)
        website.publisher = publisher

        if list_of_categories:
            website.industry.add(
                *[Industry.objects.get_or_create(industry_type=industry['industry_type'],
                                                 type=industry['type'])[0]
                  for industry in list_of_categories]
            )

        publisher.is_completed_auth = 'get_code'
        publisher.save()
        website.save()
        return website
