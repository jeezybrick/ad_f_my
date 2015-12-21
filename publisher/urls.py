from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from publisher.views import *
from publisher.models import Publisher


urlpatterns = patterns('',

    url(r'^dashboard$', DashboardView.as_view(), name='publisher_dashboard'),
    # url(r'^sites/$', SitesView.as_view(), name='publisher_sites'),
    # url(r'^sites/add-sites/$', AddSitesView.as_view(), name='publisher_add_sites'),
    url(r'^sites/edit-sites/(?P<pk>\w+)/$', EditSitesView.as_view(), name='publisher_edit_sites'),
    url(r'^audience/$', AudienceView.as_view(), name='publisher_audience'),
    url(r'^audience/(?P<pk>\w+)/$', AudienceView.as_view(), name='publisher_audience_id'),
    url(r'^export/audience/(?P<pk>\w+)/$', ExportAudience.as_view(), name='publisher_audience_export'),
    url(r'^faq$', TemplateView.as_view(template_name="publisher/faq.html"), name='publisher_faq'),
    url(r'^change-password/$',ChangePassword.as_view(), kwargs={'model': Publisher}, name="publisher_pass_change"),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/publisher/login'}, name='logout'),
    # url(r"^advertisers/$", AdvertisersView.as_view(), name='advertisers'),
    # url(r"^advertisers/$", TemplateView.as_view(template_name="publisher/index.html"), name='advertisers'),
    url(r"^sites/get-code/$", GetCodeView.as_view(), name='get-code'),
    url(r"^profile/$", ProfileView.as_view(), name='publisher-profile'),
    url(r'^$', login_required(TemplateView.as_view(template_name="publisher/index.html"), login_url='/publisher/login/'), name='publisher_dashboard'),

)
