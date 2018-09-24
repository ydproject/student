#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import classes, student
# Create your views here.


# 登录
def login(request):
    return render(request, 'login.html')


# 学生信息页面
def studentsinfo(request):
    class_names = classes.objects.all()
    context = {'currentMenu': 'studentsinfo', 'classes': class_names}
    return render(request, 'studentsinfo.html', context)

# 退出登录
def logout(request):
    if request.session.get('login_username', False):
        del request.session['login_username']
    return HttpResponseRedirect(reverse('stuMgr:login'))


# 新增新生信息界面
def addstudent(request):
    classes_info = classes.objects.all().order_by('class_name')
    if len(classes_info) == 0:
        return HttpResponseRedirect('/admin/stuMgr/classes/add/')

    context = {'currentMenu': 'studentsinfo', 'AllClassesInfo': classes_info}
    return render(request, 'addstudent.html', context)

