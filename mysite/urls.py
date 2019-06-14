

from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    re_path(r'^cycle/', include('cycle.urls')),
    re_path(r'^testing/', include('testing.urls')),
    re_path('admin/', admin.site.urls),

]
