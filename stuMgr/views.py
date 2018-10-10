#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from .models import classes, student, TermInfo
# Create your views here.


# 登录
def login(request):
    return render(request, 'login.html')


# 学生信息页面
def studentsinfo(request):
    class_names = classes.objects.all()
    context = {'currentMenu': 'studentsinfo', 'classes': class_names}
    return render(request, 'studentsinfo.html', context)

# 学费信息页面
def moneysinfo(request):
    terminfos = TermInfo.objects.all()
    context = {'currentMenu': 'moneysinfo', 'terminfos': terminfos}
    return render(request, 'moneyinfo.html', context)

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


# 编辑学生详细信息
def studetail(request, stuId):
    classes_info = classes.objects.all().order_by('class_name')
    if len(classes_info) == 0:
        return HttpResponseRedirect('/admin/stuMgr/classes/add/')
    studentInfo = get_object_or_404(student, id=stuId)
    context = {}
    context["id"] = studentInfo.id
    context["name"] = studentInfo.name
    context["tel_num"] = studentInfo.tel_num
    context["card_id"] = studentInfo.card_id
    context["birthday"] = studentInfo.birthday
    context["classid"] = studentInfo.classid
    context["sex"] = studentInfo.sex
    context["fa_name"] = studentInfo.fa_name
    context["school_car"] = studentInfo.school_car
    context["is_shuangliu"] = studentInfo.is_shuangliu
    context["is_chengdu"] = studentInfo.is_chengdu
    context["infos"] = studentInfo.infos
    context["address"] = studentInfo.address
    context["remark"] = studentInfo.remark
    context["AllClassesInfo"] = classes_info
    return render(request, 'studetail.html', context)
