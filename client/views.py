import uuid
from datetime import datetime
from django.utils.timezone import utc
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from client.forms import LoginForm, SignUpForm, ResetPasswordForm
from django.contrib import messages
from client.models import UserToken, SaveReward, RedeemCoupon
from campaign.models import Campaign, Widget, CampaignTracker


class Validate():
    """
    This class inherits it's attributes to validate the number of coupons
    available and last date of displaying the campaign
    """

    def check(self, coupon, end_date):
        """
        This method validates the coupons available and last date and returns
        a boolean value
        """

        now = datetime.utcnow()
        time = (end_date - now)

        if coupon > 0 and time:
            return True
        else:
            return False

    def get_error_message(self, check):
        """
        Would return the error message for already redeemed coupons
        """

        messages.error(self.request, "Coupon does not exists/redeemed.")
        return reverse('dashboard')


class LoginPageView(FormView):
    """
    Would help to render user login form and validate the user.
    """

    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):

        self.log_campaign_visit()
        # if user is already logged in then then redirect to success url.
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Would help to validate user and login the user.
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(self.get_success_url())

            messages.error(request, "Wrong Email and Password combination.")
            return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """

        query_string = self.request.META['QUERY_STRING'] or ''
        context['query_string'] = query_string
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
            **response_kwargs)

    def get_success_url(self):
        """
        Would return the success url depending on the whether query url is available.
        """

        if self.request.META['QUERY_STRING']:
            try:
                self.user_token_id = self.set_token_info(self.request.user)
                return reverse('outstanding_offers', args=[self.user_token_id])
            except Exception:
                messages.error(self.request, "Coupon does not exists/redeemed.")
                return reverse('dashboard')
        else:
            return reverse('dashboard')

    def set_token_info(self, user):
        """
        Would check if token is available for the user,
        else would create a token and return the id.
        """

        widget_id = self.request.GET.get('wid', '')
        reference_url = self.request.GET.get('ref_url', '')
        ad_slice = self.request.GET.get('adpart', '')
        ad_token = self.request.GET.get('adftoken', '')
        widget = Widget.objects.get(token=widget_id)
        query_data = {'user': user, 'widget': widget, 'campaign': widget.campaign, 'reference_url': reference_url}

        # if no enter is available in usertoken, then make an entry
        # and get the object.
        user_token_obj, created = UserToken.objects.get_or_create(**query_data)

        if user_token_obj.is_redeemed and not user_token_obj.is_available:
            raise Exception("Coupon does not exists/redeemed.")

        # setting the user date as utc.
        today = datetime.utcnow().replace(tzinfo=utc).date()

        # if the user already has token, will check if
        # the token exists else we will insert it.
        if user_token_obj.token is not None and not created:
            if ad_token not in user_token_obj.token:
                user_token_obj.token.append(ad_token)
                user_token_obj.save()
        else:
            token_data = [ad_token]
            user_token_obj.token = token_data
            user_token_obj.last_viewed = today
            user_token_obj.day = 1
            user_token_obj.save()

        # if the last ad view date is not today, we will set it today
        # and increase day counter by 1.
        if user_token_obj.last_viewed != today:
            user_token_obj.last_viewed = today
            user_token_obj.day = user_token_obj.day + 1
            user_token_obj.save()

        return user_token_obj.id

    def log_campaign_visit(self):
        """
        Would make a log in DB of user's campaign visit
        """

        parameter_dict = QueryDict(self.request.META['QUERY_STRING'])
        widget_id = parameter_dict.get('wid', '')

        try:
            widget = Widget.objects.get(token=widget_id)
        except:
            return

        ad_part = parameter_dict.get('adpart', '')
        reference_url = parameter_dict.get('ref_url', '')
        reference_token = parameter_dict.get('adftoken', '')
        query_dict = {'widget': widget, 'campaign': widget.campaign, 'ad_part': ad_part, 'reference_url': reference_url,
            'reference_token': reference_token}
        CampaignTracker.objects.create(**query_dict)


class SignUpPageView(FormView):
    """
    Would help to render the sign up form and create new user.
    """

    template_name = 'signup.html'
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        """
        Would help to create user.
        """

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """
        Would return the success url depending on the whether query url is available.
        """

        if self.request.META['QUERY_STRING']:
            return '%s?%s' % (reverse('login'), self.request.META['QUERY_STRING'])
        else:
            return reverse('login')

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """

        query_string = self.request.META['QUERY_STRING'] or ''
        context['query_string'] = query_string
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
            **response_kwargs)


class DashboardPageView(TemplateView):
    """
    Would render the user dashboard.
    """

    template_name = 'dashboard.html'

    def render_to_response(self, context, **response_kwargs):
        context['user_token'] = UserToken.objects.filter(is_available=True, is_redeemed=False)

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
            **response_kwargs)


class OutStandingOffersPageView(TemplateView, Validate):
    """
    Would render the user dashboard.
    """

    template_name = 'drag.html'

    def post(self, request, *args, **kwargs):
        user_token_obj = UserToken.objects.get(pk=kwargs.get('pk'))
        coupons_available = user_token_obj.campaign.coupons_available
        end_date = user_token_obj.campaign.end_date

        check = Validate.check(self, coupons_available, end_date)

        if check:
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    query_dict = {'usertoken': user_token_obj, 'coupon_part': key, 'coupon_class': value, }
                    save_reward_obj, created = SaveReward.objects.get_or_create(**query_dict)
                    if created:
                        user_token_obj.saved_pieces += 1
                        today = datetime.utcnow().replace(tzinfo=utc).date()
                        # d = today.strftime("20%y-%m-%d")
                        user_token_obj.last_saved = today
                        user_token_obj.save()
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(Validate.get_error_message(self, check))

    def render_to_response(self, context, **response_kwargs):

        if context.get('pk') is not None:
            try:
                user_token_obj = UserToken.objects.get(pk=context.get('pk'), is_redeemed=False, is_available=True)
            except:
                messages.error(self.request, "Coupon does not exists.")
                return HttpResponseRedirect("/outStandingOffers/")

            campaign_token = user_token_obj.campaign.token
            context['adfdy'] = user_token_obj.day
            context['image_path'] = "campaign/" + campaign_token + "/"
            context['save_coupon_parts'] = SaveReward.objects.filter(usertoken=user_token_obj)
            context['coupon_count'] = context['save_coupon_parts'].count()
            context['last_saved'] = user_token_obj.last_saved.strftime("20%y-%m-%d")

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
            **response_kwargs)


class CouponRedeemedPageView(TemplateView, Validate):
    template_name = 'redeemed_coupon.html'

    def post(self, request, *args, **kwargs):

        user_token_obj = UserToken.objects.get(pk=request.POST.get('user_token'))
        coupons_available = user_token_obj.campaign.coupons_available
        end_date = user_token_obj.campaign.end_date

        check = Validate.check(self, coupons_available, end_date)

        if check:
            user_token_obj.campaign
            RedeemCoupon.objects.get_or_create(usertoken=user_token_obj, user=request.user)
            user_token_obj.campaign.coupons_available = coupons_available - 1
            user_token_obj.campaign.save()
            user_token_obj.is_redeemed = True
            user_token_obj.is_available = False
            user_token_obj.save()
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect(Validate.get_error_message(self, check))

    def render_to_response(self, context, **response_kwargs):
        redeem_list = []
        redeem_coupon = RedeemCoupon.objects.filter(user=self.request.user)

        for data in redeem_coupon:
            res_data = {'campaign_name': data.usertoken.campaign.campaign_name,
                'campaign_image': data.usertoken.campaign.image, 'redeem_on': data.redeem_on, }
            redeem_list.append(res_data)

        context['redeem_list'] = redeem_list
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, template=self.get_template_names(), context=context,
            **response_kwargs)


class ChangePasswordPageView(FormView):
    form_class = ResetPasswordForm
    template_name = 'reset_password.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)

        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return self.form_invalid(form)
