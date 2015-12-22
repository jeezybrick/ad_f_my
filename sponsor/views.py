import calendar
from django.contrib.auth.hashers import make_password
from adfits import constants
from django.views.generic import View
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from publisher.models import Publisher, Website
from campaign.forms import CampaignForm, SponsorCampaignForm
from campaign.models import CampaignTracker, Campaign
from client.models import (UserToken, CampaignNotifier, SocialShare, NotificationTracker)
from sponsor.models import Sponsor
from bson import ObjectId
from login.forms import ResetPasswordForm


class SponsorMixin(View):
    """
    Validate the session for user type sponsor.
    """

    def dispatch(self, *args, **kwargs):

        if self.request.session.has_key('_id') and self.request.session.has_key('user_type'):

            # checking the type of user and responding accordingly
            if self.request.session['user_type'] == constants.USER_SPONSOR:
                return super(SponsorMixin, self).dispatch(*args, **kwargs)
            elif self.request.session['user_type'] == constants.USER_PUBLISHER:
                return HttpResponseRedirect(reverse('publisher_dashboard'))
        else:
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(reverse('sponsor_login'))


class DashboardView(SponsorMixin, TemplateView):
    """
    Would help to render the publisher dashboard
    """

    template_name = 'sponsor/dashboard.html'

    def render_to_response(self, context, **response_kwargs):
        sponsor_id = self.request.session.get('_id', '')
        tracker_obj = CampaignTracker.objects.filter(sponsor_id=sponsor_id)
        notification_tracker_obj = NotificationTracker.objects.filter(sponsor_id=sponsor_id)
        notify_type = "coupon"
        context['brand_view'] = tracker_obj.filter(action='vd').count()
        context['brand_click'] = tracker_obj.filter(action='cd').count()
        context['redeemed'] = UserToken.objects.filter(is_redeemed='true').count()
        context['brand_reminder'] = notification_tracker_obj.filter(notify_type="coupon").count()
        context['twitter_shares'] = SocialShare.objects.filter(sponsor_id=sponsor_id, social_type="twitter").count()
        context['future_rewards'] = notification_tracker_obj.filter(notify_type="campaign").count()
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   **response_kwargs)


class CampaignView(SponsorMixin, TemplateView):
    """
    Would help to render Websites for the perticular publisher
    """

    template_name = 'sponsor/campaigns.html'

    def render_to_response(self, context, **response_kwargs):
        user_id = self.request.session.get('_id', '')
        sponsor_obj = Sponsor.objects.get(pk=user_id)
        all_campaign = Campaign.objects.filter(sponsor=user_id)

        # Setting the available campaign for the sponsor
        context['campaign_list'] = [
            {'campaign_name': data.campaign_name, 'publisher': data.publisher, 'image': data.image,
             'budget': (data.coupons_available) * 5, 'start_date': data.start_date, 'end_date': data.end_date,
             'id': data.pk, } for data in all_campaign]

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   **response_kwargs)


class AddCampaignView(SponsorMixin, FormView):
    """
    Would add new websites.
    """

    template_name = 'sponsor/add_campaign.html'
    form_class = SponsorCampaignForm

    def post(self, request, *args, **kwargs):
        """
        would make an entry in the campaign collection.     
        """

        user_id = request.session.get('_id', '')
        sponsor_obj = Sponsor.objects.get(pk=user_id)
        sponsor_value = Campaign(sponsor=sponsor_obj)
        form = self.form_class(request.POST, request.FILES, instance=sponsor_value)

        if form.is_valid():
            try:
                campaign_obj = form.save()
                return HttpResponseRedirect(reverse('sponsor_campaigns'))
            except:
                import sys
                print sys.exc_value
                messages.error(request, "Unable to save the campaign")
                return self.form_invalid(form)
        else:
            messages.error(request, "Unable to save the campaign")
            return self.form_invalid(form)


class EditCampaignView(SponsorMixin, UpdateView):
    template_name = 'sponsor/edit-campaign.html'
    form_class = SponsorCampaignForm

    model = Campaign

    def get_success_url(self):
        """
        Would return the success url.
        """

        return reverse('sponsor_campaigns')


class ReportView(SponsorMixin, TemplateView):
    template_name = 'sponsor/report.html'

    def render_to_response(self, context, **response_kwargs):
        campaign_id = context.get('pk', '')
        user_id = self.request.session.get('_id', '')
        sponsor_obj = Sponsor.objects.get(pk=user_id)

        if campaign_id:
            tracker_obj = CampaignTracker.objects.filter(sponsor_id=user_id, campaign_id=campaign_id)
            notification_tracker_obj = NotificationTracker.objects.filter(sponsor_id=user_id, campaign_id=campaign_id)
            context['brand_view'] = tracker_obj.filter(action='vd').count()
            context['brand_click'] = tracker_obj.filter(action='cd').count()
            context['redeemed'] = UserToken.objects.filter(is_redeemed='true', campaign_id=campaign_id).count()
            context['brand_reminder'] = notification_tracker_obj.filter(notify_type="coupon").count()
            context['twitter_shares'] = SocialShare.objects.filter(sponsor_id=user_id, social_type="twitter").count()
            context['future_rewards'] = notification_tracker_obj.filter(notify_type="campaign").count()

        all_campaign = Campaign.objects.filter(sponsor_id=user_id)
        # Setting the available campaign for the sponsor
        context['campaign_list'] = [
            {'campaign_name': data.campaign_name, 'id': data.pk, 'selected': True if data.pk == campaign_id else False}
            for data in all_campaign]

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
                                   **response_kwargs)


class ChangePassword(FormView):
    template_name = 'sponsor/reset_password.html'
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

        return reverse('sponsor_dashboard')
