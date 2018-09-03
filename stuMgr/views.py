#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.


# 登录
def login(request):
    return render(request, 'login.html')


# 学生信息页面
def studentsinfo(request):
    context = {'currentMenu': 'studentsinfo'}
    return render(request, 'studentsinfo.html', context)

# 退出登录
def logout(request):
    if request.session.get('login_username', False):
        del request.session['login_username']
    return HttpResponseRedirect(reverse('stuMgr:login'))