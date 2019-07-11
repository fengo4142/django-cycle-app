from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from cycle.views import CycleTransactionCreate
from cycle import views

urlpatterns = [
    path('', CycleTransactionCreate.as_view()),
    path('CycleTransactionGet', views.CycleTransactionGet, name='CycleTransactionGet'),
    path('saveData', views.saveData, name='saveData'),

    path('sample_size', views.sample_size, name='sample_size'),
    path('upload_sample', views.upload_sample, name='upload_sample'),
    path('sugg_samples', views.sugg_samples, name='sugg_samples'),
    path('deficiency', views.deficiency, name='deficiency'),
    path('report_form', views.report_form, name='report_form'),
    url(r'^(?P<id>\d+)/edit/$', views.TOC_update, name='TOC_update'),

]
