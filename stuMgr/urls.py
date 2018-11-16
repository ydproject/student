# -*- coding: UTF-8 -*- 

from django.conf.urls import url, include
from . import views, views_ajax
from django.conf import settings

urlpatterns = [
    url(r'^$', views.studentsinfo, name='studentsinfo'),
    url(r'^login/$', views.login, name='login'),
    url(r'^studentsinfo/$', views.studentsinfo, name='studentsinfo'),
    url(r'^premoney/$', views.premoney, name='premoney'),
    url(r'^moneyflow/$', views.moneyflow, name='moneyflow'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addstudent/$', views.addstudent, name='addstudent'),
    url(r'^studetail/(?P<stuId>[0-9]+)/$', views.studetail, name='studetail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^moneysinfo/$', views.moneysinfo, name='moneysinfo'),
    url(r'^addmoney/$', views.addmoney, name='addmoney'),

    url(r'^authenticate/$', views_ajax.authenticateEntry, name='authenticate'),
    url(r'^getstudentsinfo/$', views_ajax.getstudentsinfo, name='getstudentsinfo'),
    url(r'^getmoneyflow/$', views_ajax.getmoneyflow, name='getmoneyflow'),
    url(r'^getpremoney/$', views_ajax.getpremoney, name='getpremoney'),
    url(r'^delstudent/$', views_ajax.delstudent, name='delstudent'),
    url(r'^modifypremoney/$', views_ajax.modifypremoney, name='modifypremoney'),
    url(r'^addstutodb/$', views_ajax.addstutodb, name='addstutodb'),
    url(r'^upload/$', views_ajax.upload, name='upload'),
    url(r'^importexcel/$', views_ajax.importexcel, name='importexcel'),
    url(r'^getmoneysinfo/$', views_ajax.getmoneysinfo, name='getmoneysinfo'),
    url(r'^getregister/$', views_ajax.getregister, name='getregister'),
    url(r'^addmoneytodb/$', views_ajax.addmoneytodb, name='addmoneytodb'),
    url(r'^seladdmoney/$', views_ajax.seladdmoney, name='seladdmoney'),
]

