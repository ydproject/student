# -*- coding: UTF-8 -*- 

from django.conf.urls import url, include
from . import views, views_ajax
from django.conf import settings

urlpatterns = [
    url(r'^$', views.studentsinfo, name='studentsinfo'),
    url(r'^login/$', views.login, name='login'),
    url(r'^studentsinfo/$', views.studentsinfo, name='studentsinfo'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addstudent/$', views.addstudent, name='addstudent'),

    url(r'^authenticate/$', views_ajax.authenticateEntry, name='authenticate'),
    url(r'^getstudentsinfo/$', views_ajax.getstudentsinfo, name='getstudentsinfo'),
    url(r'^delstudent/$', views_ajax.delstudent, name='delstudent'),
    url(r'^addstutodb/$', views_ajax.addstutodb, name='addstutodb'),
]

