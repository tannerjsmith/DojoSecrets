from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process), 
    url(r'^login$', views.login),
    url(r'^wall$', views.wall),
    url(r'^addmessage$', views.addmessage),
    url(r'^wall/popular$', views.popular),

    url(r'^wall/(?P<postid>\d+)/(?P<userid>\d+)$', views.like)

] 