import calendar
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from publisher.models import Publisher, Website
from publisher.forms import WebsiteForm
from campaign.models import CampaignTracker, Campaign
from client.models import UserToken
from bson import ObjectId



class DashboardView(TemplateView):
	"""
	Would help to render the publisher dashboard
	"""

	template_name = 'publisher/dashboard.html'

	def render_to_response(self, context, **response_kwargs):

		user_id = self.request.session.get('_id', '')
		
		context['coupons_redeemed'] = (UserToken.objects.filter(is_redeemed='true').count()) * 5
		context['campaign'] = Campaign.objects.filter(publisher_id=user_id).count()
		total_view_count, company_list, campaign_list = self.map_data(user_id)
		context['count'] = total_view_count
		context['company_list'] = company_list
		context['campaign_list'] = campaign_list
		response_kwargs.setdefault('content_type', self.content_type)
		return self.response_class(
			request = self.request,
			template = self.get_template_names(),
			context = context,
			**response_kwargs
		)

	def map_data(self, user_id):
		template_name = 'publisher/dashboard.html'

		company_map = """function() {
			var key = this.clicked_on.getMonth();
			var value = this._id;
			emit( key, value );
		}"""

		campaign_map = """function() {
			var key = this.created_on.getMonth();
			var value = this._id;
			emit( key, value );
		}"""

		campaign_reduce = """function(key, value) {
			print(key)
			return value.length
		}"""

		campaign_obj = Campaign.objects.filter(publisher_id=user_id)
		all_campaign_ids = campaign_obj.values_list('id', flat=True)
		campaign_ids = [ObjectId(str(campaign_id)) for campaign_id in all_campaign_ids]
		company_performance = CampaignTracker.objects.map_reduce(
			company_map, campaign_reduce, 
			out="temp", 
			query={'campaign_id' : {'$in' : campaign_ids}}, 
			delete_collection=True
		)

		total_view_count = CampaignTracker.objects.raw_query(
			{'campaign_id' : {'$in' : campaign_ids}}
		).count()

		company_list = [['Month', 'Traffic', { 'role': 'style' }]]
		[company_list.append(
			[calendar.month_abbr[int(data.key) + 1], round((data.value/total_view_count) * 100, 2), "blue"]
		) for data in company_performance]
		
		##campaign map	
		campaign_data = Campaign.objects.filter(publisher_id=user_id).map_reduce(
			campaign_map, campaign_reduce, 
			out="tempo", delete_collection=True
		)
                
                campaign_list = [['Month', 'Campaigns', { 'role': 'style' }]]
		
		[campaign_list.append(
			[calendar.month_abbr[int(data.key) + 1], int(data.value), "blue"]
		) for data in campaign_data ]
		return total_view_count, company_list, campaign_list


class SitesView(TemplateView):
	"""
	Would help to render Websites for the perticular publisher
	"""

	template_name = 'publisher/sites.html'

	def render_to_response(self, context, **response_kwargs):
		user_id = self.request.session.get('_id', '')
		publisher_obj = Publisher.objects.get(pk=user_id)
		all_website = publisher_obj.website
		sites = Website.objects.filter(pk__in=all_website)

		#Setting the available sites for the publisher
		context['site_list'] = [{
			'website_domain': data.website_domain,
			'website_name': data.website_name,
			'logo': data.website_logo,
			'industry': data.industry,
		} for data in sites]
			
		response_kwargs.setdefault('content_type', self.content_type)
		return self.response_class(
		    request = self.request,
			template = self.get_template_names(),
			context = context,
			**response_kwargs
		)


class AddSitesView(FormView):
	"""
	Would add new websites.
	"""

	template_name = 'publisher/add_site.html'
	form_class = WebsiteForm
	
	def post(self, request, *args, **kwargs):
		"""
		would make an entry in the website collection.		
		"""
		
		form = self.form_class(request.POST, request.FILES)

		if form.is_valid():
			try:
				website_obj = form.save()
				user_id = request.session.get('_id', '')
				publisher_obj = Publisher.objects.get(pk=user_id)
				publisher_obj.website.append(website_obj.id)
				publisher_obj.save()
				return HttpResponseRedirect(reverse('publisher_sites'))
			except:
				messages.error(request, "Unable to save the website.")
				return self.form_invalid(form)
		else:
			return self.form_invalid(form)


class AudienceView(TemplateView):
	
	template_name = 'publisher/publisher_audience.html'

	def render_to_response(self, context, **response_kwargs):
		user_id = self.request.session.get('_id', '')
		publisher_obj = Publisher.objects.get(pk=user_id)
		all_website = publisher_obj.website
		sites = Website.objects.filter(pk__in=all_website)

		#Setting the available sites for the publisher
		context['site_list'] = [{
			'website_domain': data.website_domain,
			'website_name': data.website_name,
			'logo': data.website_logo,
			'industry': data.industry,
		} for data in sites]
			
		response_kwargs.setdefault('content_type', self.content_type)
		return self.response_class(
		    request = self.request,
			template = self.get_template_names(),
			context = context,
			**response_kwargs
		)
