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


# 提交学生信息到数据库
def addstutodb(request):
    name = request.POST.get('name', '').strip()
    tel_num = request.POST.get('tel_num', '').strip()
    card_id = request.POST.get('card_id', '').strip()
    birthday = request.POST.get('birthday', '')
    classid = request.POST.get('classid', '')
    sex = request.POST.get('sex', '')
    fa_name = request.POST.get('fa_name', '').strip()
    school_car = request.POST.get('school_car', '').strip()
    is_shuangliu = request.POST.get('is_shuangliu', '')
    is_chengdu = request.POST.get('is_chengdu', '')
    infos = request.POST.get('infos', '').strip()
    address = request.POST.get('address', '').strip()
    remark = request.POST.get('remark', '').strip()

    if len(tel_num) != 11:
        context = {'errMsg': '联系电话输入不正确!'}
        return render(request, 'error.html', context)
    if len(card_id) != 18:
        context = {'errMsg': '身份证号码输入不正确!'}
        return render(request, 'error.html', context)
    if student.objects.filter(card_id=card_id):
        context = {'errMsg': '该身份证号码的学生已存在!'}
        return render(request, 'error.html', context)

    try:
        Student = student(name=name,tel_num=tel_num, card_id=card_id, birthday=birthday, classid_id=classid, sex=sex, fa_name=fa_name,
                school_car=school_car, is_shuangliu=is_shuangliu, is_chengdu=is_chengdu, infos=infos, address=address, remark=remark)
        Student.save()
    except Exception as msg:
        import traceback
        print(traceback.format_exc())
        context = {'errMsg': '添加学生信息失败，请联系管理员处理!'}
        return render(request, 'error.html', context)

    return HttpResponseRedirect(reverse('stuMgr:studentsinfo'))
