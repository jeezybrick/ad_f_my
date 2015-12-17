import json
from django.http import HttpResponse

from campaign.models import Campaign
from publisher.models import Publisher, Website
from django.core.exceptions import ObjectDoesNotExist
from bson import ObjectId


def get_websites(request):
	"""
	Would help to get the website depending on the publisher.
	"""

	if request.is_ajax() or request.GET:
		campaign_id = request.GET.get('cid')
		publisher_id = request.GET.get('pid')

		try:
			id_campaign = 0

			if campaign_id not in ['', 'add']:
				campaign_obj = Campaign.objects.get(pk=campaign_id)
				
				if campaign_obj.website is not None:
					id_campaign = campaign_obj.website.pk
			
			publisher_obj = Publisher.objects.get(id=publisher_id)
			website = Website.objects.filter(pk__in=publisher_obj.website)
			website_list = [[data.pk, data.website_name, 
				True if id_campaign == data.pk else False
			] for data in website ]
		except Campaign.DoesNotExist:
			publisher_obj = Publisher.objects.get(id=publisher_id)
			website = Website.objects.filter(pk__in=publisher_obj.website)
			website_list = [[data.pk, data.website_name, False
			] for data in website ]
		except Publisher.DoesNotExist:
			website_list = []
		except:
			website_list = []

	response = {
		'status': True,
		'website_list': website_list
	}
	return HttpResponse(
		json.dumps(response),
		content_type = 'application/javascript; charset=utf8'
	)