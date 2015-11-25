from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from sponsor.models import Sponsor
from sponsor.views import *


urlpatterns = patterns('',
    url(r'^dashboard$', DashboardView.as_view(), name='sponsor_dashboard'),
    url(r'^campaigns$', CampaignView.as_view(), name='sponsor_campaigns'),
    url(r'^campaigns/add-campaign$', AddCampaignView.as_view(), name='sponsor_add_campaign'),
    url(r'^campaigns/edit-campaign/(?P<pk>\w+)/$', EditCampaignView.as_view(), name='sponsor_edit_campaign'),
    url(r'^reports/$', ReportView.as_view(), name='sponsor_report'),
    url(r'^report/(?P<pk>\w+)/$', ReportView.as_view(), name='sponsor_report_id'),
    url(r'^faq$', TemplateView.as_view(template_name="sponsor/faq.html"), name='sponsor_faq'),
    url(r'^change-password/$',ChangePassword.as_view(), kwargs={'model': Sponsor}, name="sponsor_pass_change"),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/sponsor/login'}, name='logout')
)
