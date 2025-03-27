from django.contrib import admin
from django.urls import path

from _core.api import api as _core_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", _core_api.urls),
]
