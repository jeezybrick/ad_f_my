from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core import forms, utils
from my_auth.models import MyUser
from publisher.forms import WebsiteNewForm
from publisher.models import Publisher, Website
from adfits import constants


# For redirect if not Auth
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/publisher/login')


# For login
class HomeView(View):
    form_class = forms.DemoForm
    template_name = 'home.html'
    title = _('Home')

    def get(self, request):

        form = self.form_class()
        context = {
            'form': form,
            'title': self.title,
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        context = {
            'form': form,
            'title': self.title,
        }
        if form.is_valid():
            utils.send_email_with_form_data(request.POST)
            return redirect(self.get_success_url())
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("thanks")


class JoinNetworkView(View):
    template_name = 'join_network.html'
    title = _('Join network')
    form_class = forms.JoinNetworkForm

    def get(self, request):

        form = self.form_class()
        context = {
            'form': form,
            'title': self.title,
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)

        context = {
            'form': form,
            'title': self.title,
        }
        if form.is_valid():
            form.save()
            # utils.send_email_with_form_data_join(request.POST)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
            messages.error(request, "Wrong username and Password combination.")
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("advertisers")

