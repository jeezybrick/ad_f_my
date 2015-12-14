from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core import views
from client.views import *
from login.views import *
from campaign.ajax import get_websites
from sponsor.models import Sponsor
from publisher.models import Publisher

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sponsor/login$', LoginView.as_view(), kwargs={'model': Sponsor}, name='sponsor_login'),
    url(r'^publisher/login$', LoginView.as_view(), kwargs={'model': Publisher}, name='publisher_login'),
    url(r'^publisher/', include('publisher.urls')),
    url(r'^sponsor/', include('sponsor.urls')),
    url(r'^campaign/get-websites/$', get_websites),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^help$', TemplateView.as_view(template_name="help.html"), name='help'),
    url(r'^test$', TemplateView.as_view(template_name="test.html"), name='test'),
    url(r'^policy$', TemplateView.as_view(template_name="policy.html"), name='policy'),
    url(r'^policy_two$', TemplateView.as_view(template_name="policy_two.html"), name='policy_two'),
    url(r'^terms$', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^terms_two$', TemplateView.as_view(template_name="terms_two.html"), name='terms_two'),
    url(r'^thanks$', TemplateView.as_view(template_name="thanks.html"), name='thanks'),
    url(r'^faq$', TemplateView.as_view(template_name="faq.html"), name='faq'),
    url(r"^join-network/$", views.JoinNetworkView.as_view(), name='join-network'),
    url(r'^signUp$', SignUpPageView.as_view(), name='signup'),
    url(r'^outStandingOffers/$', login_required(DashboardPageView.as_view()), name='dashboard'),
    url(r'^outStandingOffers/(?P<pk>\w+)/$', login_required(OutStandingOffersPageView.as_view()), name='outstanding_offers'),
    url(r'^couponsRedeemed/$', login_required(CouponRedeemedPageView.as_view()), name='coupons_redeemed'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout')
)

urlpatterns += patterns('', 
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT
	}),
)
