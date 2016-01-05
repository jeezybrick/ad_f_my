from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core import forms, utils


# For redirect if not Auth
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/publisher/login')


# For login
class HomeView(FormView):
    form_class = forms.DemoForm
    template_name = 'home.html'
    success_url = reverse_lazy("thanks")

    def form_valid(self, form):
        utils.send_email_with_form_data(self.request.POST)
        return super(HomeView, self).form_valid(form)


class JoinNetworkView(FormView):
    template_name = 'join_network.html'
    form_class = forms.JoinNetworkForm
    success_url = '/publisher/#/advertisers/'

    def form_valid(self, form):
        form.save()
        form.send_email()

        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(email=email, password=password)

        if user is not None:

            from allauth.account.utils import complete_signup
            from allauth.account import app_settings
            complete_signup(self.request, user, app_settings.EMAIL_VERIFICATION, '/')

            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        # messages.error(self.request, "Wrong username and Password combination.")
        return super(JoinNetworkView, self).form_valid(form)
