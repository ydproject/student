#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from .models import classes, student, TermInfo, Payment_Plan, users, PayMentInfo, Payment_item
# Create your views here.


# 登录
def login(request):
    return render(request, 'login.html')


# 学生信息页面
def studentsinfo(request):
    class_names = classes.objects.all()
    context = {'currentMenu': 'studentsinfo', 'classes': class_names}
    return render(request, 'studentsinfo.html', context)

# 学生预收费信息
def premoney(request):
    class_names = classes.objects.all()
    context = {'currentMenu': 'premoney', 'classes': class_names}
    return render(request, 'premoney.html', context)

# 缴费流水信息
def moneyflow(request):
    context = {'currentMenu': 'moneyflow'}
    return render(request, 'moneyflow.html', context)

# 学费信息页面
def moneysinfo(request):
    terminfos = TermInfo.objects.all()
    class_names = classes.objects.all()
    pay_types = Payment_item.objects.all()
    context = {'currentMenu': 'moneysinfo',
               'terminfos': terminfos,
               'pay_types': pay_types,
               'classes': class_names}
    return render(request, 'moneyinfo.html', context)

# 学生报名/缴费信息页面
def register(request):
    terminfos = TermInfo.objects.all()
    class_names = classes.objects.all()
    context = {'currentMenu': 'register', 'terminfos': terminfos, 'classes': class_names}
    return render(request, 'register.html', context)

# 退出登录
def logout(request):
    if request.session.get('login_username', False):
        del request.session['login_username']
    return HttpResponseRedirect(reverse('stuMgr:login'))


# 新增新生信息界面
def addstudent(request):
    add_type = request.GET.get("type", "")
    classes_info = classes.objects.all().order_by('class_name')
    if len(classes_info) == 0:
        return HttpResponseRedirect('/admin/stuMgr/classes/add/')

    if add_type == "sign":
        redirect_url = '/addmoney/'
    else:
        redirect_url = '/studentsinfo/'

    context = {'currentMenu': 'studentsinfo', 'AllClassesInfo': classes_info, "redirect_url": redirect_url}
    return render(request, 'addstudent.html', context)


# 新增缴费信息界面
def addmoney(request):
    stuId = request.GET.get("id", "")
    flag = request.GET.get("flag", "")
    termName = int(request.GET.get("term", ""))
    studentInfo = get_object_or_404(student, id=stuId)
    # 获取用户信息
    loginUser = request.session.get('login_username', False)
    loginUserOb = users.objects.get(username=loginUser)
    if loginUserOb.is_superuser == 1 or loginUserOb.role == '管理员':
        allowed = "yes"
    else:
        allowed = "no"
    payMentPlan = Payment_Plan.objects.filter(flag=True).values("plan__type_info", "plan__action", "plan__money")
    payMentPlan = [{'plan__type_info': payInfo['plan__type_info'], 'plan__action': payInfo['plan__action'].split(","),
                    'plan__money': payInfo['plan__money'].split(",")} for payInfo in payMentPlan]
    if flag == "add":
        termInfos = TermInfo.objects.all().values()
        termInfo = termInfos[0]
        OldPayMentInfo = []
    elif flag == "edit":
        termInfo = get_object_or_404(TermInfo, id=termName)
        OldPayMentInfo = PayMentInfo.objects.filter(stuId=stuId, termId__term_name=termInfo).values("type", "action", "money", "status")
    else:
        return HttpResponseRedirect(reverse('stuMgr:register'))

    payMents = []
    i = 0
    for payMent in payMentPlan:
        temp = {}
        temp["f_type"] = payMent["plan__type_info"]
        temp["f_actions"] = []
        for f_action in payMent["plan__action"]:
            t_action = {}
            i = i + 1
            t_action["f_id"] = "f_id_" + str(i)
            t_action["action"] = f_action
            t_action["edit"] = 0
            t_action["status"] = []
            for f_money in payMent["plan__money"]:
                t_money = {}
                t_money["money"] = f_money
                t_money["status"] = 0
                for oldpayinfo in OldPayMentInfo:
                    if oldpayinfo["type"] == temp["f_type"] and oldpayinfo["action"] == f_action and oldpayinfo["status"] == "已缴费" and oldpayinfo["money"] == float(f_money):
                        t_money["status"] = 1
                        t_action["edit"] = 1
                t_action["status"].append(t_money)
            temp["f_actions"].append(t_action)
        payMents.append(temp)

    context = {'currentMenu': 'register',
               'TermInfo': termInfo,
               "PayMents": payMents,
               "studentInfo": studentInfo,
               "allowed": allowed,
               "index" : i,
               }
    return render(request, 'addmoney.html', context)


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
