"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
import re

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token, name='api-login'),
    path('api/', include('choir.urls')),
]

# Served unconditionally (not just when DEBUG=True, unlike the usual
# django.conf.urls.static.static() helper — it no-ops when DEBUG=False).
# This app is small and internal, with no separate media server/CDN.
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
