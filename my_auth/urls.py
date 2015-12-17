
from django.conf.urls import url
from my_auth import views


urlpatterns = [

    # Auth views
    url(r'^auth/login/$', views.LoginView.as_view(),
        name='login'),
    url(r'^auth/logout/$', views.get_logout, name='logout'),

]
