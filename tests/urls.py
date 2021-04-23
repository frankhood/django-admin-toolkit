# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django_admin_toolkit.urls', namespace='django_admin_toolkit')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
