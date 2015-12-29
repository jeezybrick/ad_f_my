
from django.conf.urls import url, include
from api import views


urlpatterns = [
    url(r'^api/publisher/$', views.CurrentPublisherDetail.as_view(), name='publisher_api'),
    url(r'^api/publisher/(?P<pk>[0-9]+)/$',
        views.CurrentPublisherDetail.as_view(), name='publisher_detail_api'),
    url(r'^api/publisher/website/$', views.PublisherWebsiteList.as_view(), name='publisher_website_api'),
    url(r'^api/publisher/website/(?P<pk>[0-9]+)/$', views.PublisherWebsiteDetail.as_view(), name='publisher_website_detail_api'),
    url(r'^api/category/$', views.CategoryList.as_view(), name='category_api'),
    url(r'^api/sponsor/$', views.AdvertisersList.as_view(), name='sponsor_api'),
    url(r'^api/complete-setup/$', views.CompleteSetupView.as_view(), name='complete_setup_api'),

    url(r'^rest-auth/', include('rest_auth.urls'))
]
