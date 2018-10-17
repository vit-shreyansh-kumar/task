from django.conf.urls import url
from . import views

app_name = 'featurerequest'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userlogin/$', views.userlogin, name='userlogin'),
    url(r'^userlogout/$', views.userlogout, name='userlogout'),
    url(r'^add/$', views.add_features, name='add_features'),
    url(r'^page/(?P<page>\d+)/$', views.index, name='index-withpage'),
]