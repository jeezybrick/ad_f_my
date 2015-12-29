from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import FormView
from login.forms import LoginForm


# For login
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/publisher/'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


# logout function
def get_logout(request):

    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
