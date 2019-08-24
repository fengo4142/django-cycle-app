from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from blog import views
    
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
]
