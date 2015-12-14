import calendar
import xlwt
from adfits import constants
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from publisher.models import Publisher, Website
from publisher.forms import PublisherWebsiteForm, ResetPasswordForm
from campaign.models import CampaignTracker, Campaign
from client.models import UserToken, RedeemCoupon
from login.forms import ResetPasswordForm
from bson import ObjectId
from login.backend import authenticate
from django.contrib.auth.models import make_password


class DashboardView(TemplateView):
    """
    Would help to render the publisher dashboard with different 
    charts to show publisher specifice activity.
    """

    template_name = 'publisher/dashboard.html'

    def render_to_response(self, context, **response_kwargs):
        user_id = self.request.session.get('_id', '')
        context['coupons_redeemed'] = RedeemCoupon.objects.count() * 5
        context['campaign'] = Campaign.objects.filter(
            publisher_id=user_id
        ).count()
        total_view_count, company_list, campaign_list, reedem_list = self.map_data(user_id)
        context['count'] = total_view_count
        context['company_list'] = company_list
        context['campaign_list'] = campaign_list
        context['reedem_list'] = reedem_list
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )

    def map_data(self, user_id):
        """
        Would prepare data for the charts to be displayed on publisher dashboard.
        """

        template_name = 'publisher/dashboard.html'

        #setting the map reduce methods.
        company_map = """function() {
            var key = this.clicked_on.getMonth();
            var value = this._id;
            if ( value instanceof Array ) {
                emit( key, value );
            } else {
                emit( key, 1)
            }
        }"""

        campaign_map = """function() {
            var key = this.created_on.getMonth();
            var value = this._id;
            if ( value instanceof Array ) {
                emit( key, value );
            } else {
                emit( key, 1)
            }
        }"""

        campaign_reduce = """function(key, value) {
            return value.length
        }"""

        notreedem_map = """function() {
            var key = this.created_on.getMonth();
            var value = this.coupons_available;

            if (isNaN(value)) {
                emit(key, 0);    
            } else {
                emit(key, value);
            }
        }"""

        notreedem_reduce = """function(key, value) {
            var sum = 0;

            for (i=1; i<=value.length; i++) {
                if (isNaN(value[i])) {
                    continue;
                }
                sum = sum + value[i];
            }
            return sum;
        }"""

        reedem_map = """function() {
            var key = this.redeem_on.getMonth();
            var value = this._id;
            emit(key, 1);                
        }"""

        reedem_reduce = """function(key, value) {
            return value.length;
        }"""

        #Setting the camapaign and campaigntracker refference.
        campaign_obj = Campaign.objects.filter(publisher_id=user_id)
        campaigntracker_obj = CampaignTracker.objects.filter(
            publisher_id=user_id, action="vd"
        )

        #getting total camapaign view for the publisher.
        total_view_count = campaigntracker_obj.count()

        #getting total camapaign view per month for the publisher.
        #(Chart 1 on dashboard)
        company_performance = campaigntracker_obj.map_reduce(
            company_map, campaign_reduce, 
            out="temp",
            delete_collection=True
        )
        
        #preparing the data to be sent for chart for campaign view per 
        #month(Chart 1 on dashboard)
        company_list = [['Month', 'Views', { 'role': 'style' }]]

        [company_list.append(
            [calendar.month_abbr[int(data.key or 0) + 1], 
            round((data.value/total_view_count) * 100, 2), ""]
        ) for data in company_performance]

        if len(company_list) == 1:
        	company_list.append([0, 0, "#5ec8f2"])
        
        #getting the data for campaign created/assigned per month to a 
        #publisher(Chart 3 on dashboard)
        campaign_data = campaign_obj.map_reduce(
            campaign_map, campaign_reduce, 
            out="temp", delete_collection=True
        )

        #preparing the data to be sent for chart for campaign created per 
        #month(Chart 3 on dashboard)
        campaign_list = [['Month', 'Campaigns', { 'role': 'style' }]]

        [campaign_list.append(
            [calendar.month_abbr[int(data.key or 0) + 1], int(data.value or 0), ""]
        ) for data in campaign_data ]

        if len(campaign_list) == 1:
       		campaign_list.append([0, 0, "#5ec8f2"])

        #getting number of coupons redeemed per month for a publisher
        coupons_redeemed = RedeemCoupon.objects.filter(
            publisher_id=user_id
        ).map_reduce(
            reedem_map, reedem_reduce, 
            out="temp", delete_collection=True
        )

        reedem_dict = {}
        #creating the for per month redeemed coupons
        [reedem_dict.update({
            str(int(data.key)): int(data.value or 0)
        }) for data in coupons_redeemed ]
        
        #getting number of coupons not redeemed per month for a publisher
        #(Chart 2 on dashboard)
        coupons_notredeemed = campaign_obj.map_reduce(
            notreedem_map, notreedem_reduce, 
            out="temp", delete_collection=True
        )

        #preparing the data to be sent for chart for coupons redeemed 
        #and not redeemed per mmonth(Chart 2 on dashboard)
        reedem_list = [['Month', 'Coupons Not Redeemed ', 'Redeemed Coupons', { 
            "role": 'annotation' }]
        ]

        not_reedem_dict = {}

        [not_reedem_dict.update({
            str(int(data.key or 0)): int(data.value or 0)
        }) for data in coupons_notredeemed ]
        
        for i in xrange(1, 13):

            if reedem_dict.get(str(i)) or not_reedem_dict.get(str(i)):
                reedem_list.append([
                    calendar.month_abbr[i], 
                    not_reedem_dict.get(str(i), 0), 
                    reedem_dict.get(str(i), 0), 
                    ""
                ])

        if len(reedem_list) ==  1:
            reedem_list.append([0, 0, 0, ""])

        return total_view_count, company_list, campaign_list, reedem_list


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
        tracker_obj = CampaignTracker.objects.filter(
            publisher_id=user_id, action="vd"
        )

        #Setting the available sites for the publisher
        context['site_list'] = [{
            'pk': data.pk,
            'website_domain': data.website_domain,
            'website_name': data.website_name,
            'logo': data.website_logo,
            'audience': tracker_obj.filter(website_id=data.pk).count(),
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
    form_class = PublisherWebsiteForm
    
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


class EditSitesView(UpdateView):
    """
    Would help to edit website info
    """

    template_name = 'publisher/edit_site.html'
    form_class = PublisherWebsiteForm
    model = Website

    def get_success_url(self):
        """
        Would return the success url.
        """

        return reverse('publisher_sites')
    

class AudienceView(TemplateView):
    """
    Would render the audience template for the publisher tab.
    """

    template_name = 'publisher/publisher_audience.html'

    def render_to_response(self, context, **response_kwargs):
        context['site_id'] = context.get('pk', 0)
        user_id = self.request.session.get('_id', '')

        try:
            #getting the publisher instance
            publisher_obj = Publisher.objects.get(pk=user_id)
            #Getting all websites by publisher
            all_website = publisher_obj.website
            sites = Website.objects.filter(pk__in=all_website)
            #Setting the available sites for the publisher
            context['site_list'] = [{
                'website_id': data.pk,
                'website_domain': data.website_domain,
                'website_name': data.website_name,
                'selected': True if data.pk == context['site_id'] else False
            } for data in sites]

            #
            if context.get('pk') is not None:
                
                website_obj = sites.filter(
                    pk=context['site_id']
                ).values_list(
                    'website_name', flat=True
                )

                if website_obj:
                    context['site_name'] = website_obj[0]
                else:
                    context['site_name'] = ''

                #Getting all campaign by publisher. 
                all_campaign_list = Campaign.objects.filter(
                    publisher=publisher_obj
                ).values_list(
                    'pk', flat=True
                )
                campaign_list = [ObjectId(data) for data in all_campaign_list]
                #Getting all the user who redeemed the coupon
                context['user_redeemed'] = UserToken.objects.raw_query({
                    'website_id': ObjectId(context['site_id']),
                    'is_redeemed': True,
                    'campaign_id': {'$in': campaign_list }
                })
            else:
                context['site_id'] = 0
        except:
            context['site_list'] = []
        
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )


class ExportAudience(TemplateView):
    """
    Would be used to export the all users who had 
    reedemed the coupon for a website.
    """

    def render_to_response(self, context, **response_kwargs):
        """
        Customized render function to response xls file(spread sheet),
        Get all the person who redeemed the coupon.
        """

        #Setting the rresponse header
        response = HttpResponse(mimetype="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % ("Audience.xls")
        counter = 0

        #Formatting the header of the spreadsheet
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Audience')
        worksheet.write(counter, 0, 'Website Name')
        worksheet.write(counter, 1, 'Email')    
        worksheet.write(counter, 2, 'First Name')
        worksheet.write(counter, 3, 'Last Name')
        worksheet.write(counter, 4, 'Gender')
        worksheet.write(counter, 5, 'Age')
        worksheet.write(counter, 6, 'Location')

        try:
            site_id = context.get('pk')
            #Getting the website refered
            sites = Website.objects.get(pk=site_id)
            user_id = self.request.session.get('_id', '')
            #Getting all campaign by publisher. 
            all_campaign_list = Campaign.objects.filter(
                publisher_id=user_id
            ).values_list(
                'pk', flat=True
            )
            campaign_list = [ObjectId(data) for data in all_campaign_list]
            #Getting all the user who redeemed the coupon
            user_redeemed = UserToken.objects.raw_query({
                'website_id': ObjectId(site_id),
                'is_redeemed': True,
                'campaign_id': {'$in': campaign_list }
            })
        except:
            user_redeemed = []
            counter += 1
            #if exception ocurred set the Data not available message.
            worksheet.write(counter, 1, "Data")
            worksheet.write(counter, 2, "not")
            worksheet.write(counter, 3, "available.")

        for data in user_redeemed:
            counter += 1
            worksheet.write(counter, 0, sites.website_name)
            worksheet.write(counter, 1, data.email) 
            worksheet.write(counter, 2, data.first_name)
            worksheet.write(counter, 3, data.last_name)
            worksheet.write(counter, 4, data.sex)
            worksheet.write(counter, 5, data.age)
            worksheet.write(counter, 6, data.location)

        workbook.save(response)
        return response


class ChangePassword(FormView):
    template_name = 'publisher/reset_password.html'
    form_class = ResetPasswordForm
    
    def post(self, request, *args, **kwargs):
        query_model = kwargs['model']
        user_id = request.session['_id']
        user_obj = query_model.objects.get(pk=user_id)

        form = self.form_class(query_model, user_obj.name, request.POST)

        if form.is_valid():
            password = form.cleaned_data['new_password']
            new_password = make_password(password, salt="adfits")
            user_obj.password = new_password
            user_obj.save()
            return HttpResponseRedirect(self.get_success_url()) 
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """
        Would return the success url depending on the whether query url is available.
        """
        
        return reverse('publisher_dashboard')


class AdvertisersView(View):
    template_name = 'advertisers.html'
    title = _('Advertisers')

    def get(self, request):
        context = {
            'title': self.title,
        }
        return TemplateResponse(request, self.template_name, context)
    '''
    def post(self, request):
        context = {
            'title': self.title,
        }
        if form.is_valid():
            return redirect(self.get_success_url())
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("get-code")

    '''
class GetCodeView(View):
    template_name = 'get_code.html'
    title = _('Get code')

    def get(self, request):
        context = {
            'title': self.title,
        }
        return TemplateResponse(request, self.template_name, context)
'''
    def post(self, request):
        context = {
            'title': self.title,
        }
        if form.is_valid():
            return redirect(self.get_success_url())
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("home")
'''