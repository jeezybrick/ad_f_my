import time
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from login.forms import LoginForm, ResetPasswordForm
from publisher.forms import AddwebsiteForm
from sponsor.models import Sponsor, Industry
from publisher.models import Publisher, Website, get_website_logo_path
from campaign.models import CampaignTracker
from django.contrib import messages
from backend import authenticate, login
from django.core.urlresolvers import reverse
from django.forms.forms import BoundField
from adfits import constants
from django.contrib.auth.models import make_password


class LoginView(FormView):
    """
    Would help to render user login form and validate the user.
    """

    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):

        # if user has the key 'user_type' then redirect to the success url.
        if request.session.get('user_type', ''):
            next = self.get_success_url()

            if next is not None:
                return HttpResponseRedirect(next)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Would help to validate user and login the user.
        """
        model = kwargs['model']

        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(model, email=email, password=password)

            if user is not None:
                login(request, user)
                request.session['_id'] = user.pk

                # if model is publisher model.
                if model == Publisher:
                    request.session['user_type'] = constants.USER_PUBLISHER
                    return HttpResponseRedirect(self.get_success_url())
                elif model == Sponsor:
                    # if model is sponsor model.
                    request.session['user_type'] = constants.USER_SPONSOR
                    return HttpResponseRedirect(self.get_success_url())
            messages.error(request, "Wrong username and Password combination.")
            return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """
        Would return the success url depending on the whether query url is available.
        """

        if self.request.session.get('user_type', '') == constants.USER_PUBLISHER:
            return reverse('publisher_dashboard')
        elif self.request.session.get('user_type', '') == constants.USER_SPONSOR:
            return reverse('sponsor_dashboard')
        else:
            return None


class ChangePassword(FormView):
    template_name = 'reset_password.html'
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

        if self.request.session.get('user_type', '') == constants.USER_PUBLISHER:
            return reverse('publisher_dashboard')
        elif self.request.session.get('user_type', '') == constants.USER_SPONSOR:
            return reverse('sponsor_dashboard')
        else:
            return None
