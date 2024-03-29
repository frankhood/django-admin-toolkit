# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
