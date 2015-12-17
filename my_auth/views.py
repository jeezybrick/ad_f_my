from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from login.forms import LoginForm
from my_auth.forms import MyLoginForm


# For login
class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'
    title = _('Sign In')

    def get(self, request):
        form = self.form_class(request)
        context = {
            'form': form,
            'title': self.title
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        context = {
            'form': form,
            'title': self.title,
        }
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("publisher_dashboard")


# logout function
def get_logout(request):

    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
