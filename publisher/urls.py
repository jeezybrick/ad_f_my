from django.conf.urls import patterns, url
from publisher.views import *
from publisher.models import Publisher


urlpatterns = patterns('',

    url(r'^export/audience/(?P<pk>\w+)/$', ExportAudience.as_view(), name='publisher_audience_export'),
    url(r'^faq$', TemplateView.as_view(template_name="publisher/faq.html"), name='publisher_faq'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/publisher/login'}, name='logout'),
    url(r'^$', PublisherIndex.as_view(), name='publisher_index'),

)
