# -*- coding: UTF-8 -*- 

from django.conf.urls import url, include
from . import views, views_ajax
from django.conf import settings

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^authenticate/$', views_ajax.authenticateEntry, name='authenticate'),
]

