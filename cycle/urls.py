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
]
