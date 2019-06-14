from django.urls import path, include
from testing import views

urlpatterns = [
    path('sample_size', views.sample_size, name='sample_size'),
    path(r'^(?P<id>\d+)/edit/$', views.TOC_update, name='TOC_update'),

]
