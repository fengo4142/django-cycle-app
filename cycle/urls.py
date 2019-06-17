from django.contrib import admin
from django.urls import path, include
from cycle.views import CycleTransactionCreate
from cycle.views import CycleTransactionCreateOld
from cycle import views

urlpatterns = [
    path('', CycleTransactionCreate.as_view()),
    path('CycleTransactionGet', views.CycleTransactionGet, name='CycleTransactionGet'),
    path('saveData', views.saveData, name='saveData'),
    path('old', CycleTransactionCreateOld.as_view()),

    path('sample_size', views.sample_size, name='sample_size'),
    path('upload_sample', views.upload_sample, name='upload_sample'),
    path('sugg_samples', views.sugg_samples, name='sugg_samples'),
    path(r'^(?P<id>\d+)/edit/$', views.TOC_update, name='TOC_update'),

]
