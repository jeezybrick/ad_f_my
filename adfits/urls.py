from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as forgot_password_views
from core import views
from client.views import *
from my_auth.views import LoginView
from campaign.ajax import get_websites
from sponsor.models import Sponsor
from publisher.models import Publisher

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sponsor/login/$', LoginView.as_view(), name='sponsor_login'),
    url(r'^publisher/login/$', LoginView.as_view(), name='publisher_login'),
    url(r'^publisher/', include('publisher.urls')),
    url(r'^sponsor/', include('sponsor.urls')),
    url(r'^campaign/get-websites/$', get_websites),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^help/$', TemplateView.as_view(template_name="help.html"), name='help'),
    url(r'^test/$', TemplateView.as_view(template_name="test.html"), name='test'),
    url(r'^policy/$', TemplateView.as_view(template_name="policy.html"), name='policy'),
    url(r'^policy_two/$', TemplateView.as_view(template_name="policy_two.html"), name='policy_two'),
    url(r'^terms/$', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^terms_two/$', TemplateView.as_view(template_name="terms_two.html"), name='terms_two'),
    url(r'^thanks/$', TemplateView.as_view(template_name="thanks.html"), name='thanks'),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"), name='faq'),
    url(r"^join-network/$", views.JoinNetworkView.as_view(), name='join-network'),
    url(r'^signUp$', SignUpPageView.as_view(), name='signup'),
    url(r'^outStandingOffers/$', login_required(DashboardPageView.as_view()), name='dashboard'),
    url(r'^outStandingOffers/(?P<pk>\w+)/$', login_required(OutStandingOffersPageView.as_view()), name='outstanding_offers'),
    url(r'^couponsRedeemed/$', login_required(CouponRedeemedPageView.as_view()), name='coupons_redeemed'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^', include('api.urls')),

    # Forgot Password Functionality
    url(r'^forgot-password/$', forgot_password_views.password_reset,
        #{'template_name': 'dashboard/forgot_password.html'},
        name='password_reset'),

    url(r'^forgot-password/done/$', forgot_password_views.password_reset_done,
        #{'template_name': 'dashboard/forgot_password_done.html'},
        name='password_reset_done'),

    url(r'^forgot-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        forgot_password_views.password_reset_confirm,
        #{'template_name': 'dashboard/forgot_password_confirm.html', },
        name='password_reset_confirm'),

    url(r'^forgot-password/success/$',forgot_password_views.password_reset_complete,
        #{'template_name': 'dashboard/forgot_password_complete.html'},
        name='password_reset_complete'),

    # Social
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^accounts/', include('allauth.urls')),


)

urlpatterns += patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': settings.MEDIA_ROOT
	}),
)
