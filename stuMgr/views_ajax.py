#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: yuandi
@file: view_ajax.py
@time: 2018/9/3 21:49
"""

import datetime
import simplejson as json
import os
import traceback

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
import pandas as pd

from .extend_json_encoder import ExtendJSONEncoder
from .models import student, classes, PayMentInfo, student_term_info, TermInfo, Flowing, PreMent, users
from .common import clear


login_failure_counter = {}

# ajax接口，登录页面调用，用来验证用户名密码
@csrf_exempt
def loginAuthenticate(username, password):
    """登录认证，包含一个登录失败计数器，5分钟内连续失败5次的账号，会被锁定5分钟"""
    lockCntThreshold = settings.LOCK_CNT_THRESHOLD
    lockTimeThreshold = settings.LOCK_TIME_THRESHOLD
    # 服务端二次验证参数
    if username == "" or password == "" or username is None or password is None:
        result = {'status': 2, 'msg': '登录用户名或密码为空，请重新输入!', 'data': ''}
    elif username in login_failure_counter and login_failure_counter[username]["cnt"] >= lockCntThreshold and (
            datetime.datetime.now() - login_failure_counter[username][
        "last_failure_time"]).seconds <= lockTimeThreshold:
        result = {'status': 3, 'msg': '登录失败超过5次，该账号已被锁定5分钟!', 'data': ''}
    else:
        # 登录
        user = authenticate(username=username, password=password)
        # 登录成功
        if user:
            # 如果登录失败计数器中存在该用户名，则清除之
            if username in login_failure_counter:
                login_failure_counter.pop(username)
            result = {'status': 0, 'msg': 'ok', 'data': user}
        # 登录失败
        else:
            if username not in login_failure_counter:
                # 第一次登录失败，登录失败计数器中不存在该用户，则创建一个该用户的计数器
                login_failure_counter[username] = {"cnt": 1, "last_failure_time": datetime.datetime.now()}
            else:
                if (datetime.datetime.now() - login_failure_counter[username][
                    "last_failure_time"]).seconds <= lockTimeThreshold:
                    login_failure_counter[username]["cnt"] += 1
                else:
                    # 上一次登录失败时间早于5分钟前，则重新计数。以达到超过5分钟自动解锁的目的。
                    login_failure_counter[username]["cnt"] = 1
                login_failure_counter[username]["last_failure_time"] = datetime.datetime.now()
            result = {'status': 1, 'msg': '用户名或密码错误，请重新输入！', 'data': ''}
    return result


# ajax接口，登录页面调用，用来验证用户名密码
@csrf_exempt
def authenticateEntry(request):
    """接收http请求，然后把请求中的用户名密码传给loginAuthenticate去验证"""
    username = request.POST.get('username')
    password = request.POST.get('password')
    result = loginAuthenticate(username, password)
    if result['status'] == 0:
        # session保存用户信息
        request.session['login_username'] = username
        result = {'status': 0, 'msg': 'ok', 'data': None}

    return HttpResponse(json.dumps(result), content_type='application/json')


# 获取学生信息列表
@csrf_exempt
def getstudentsinfo(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)

    limit = int(request.POST.get('limit', 0))
    offset = int(request.POST.get('offset', 0))
    if limit == 0 and offset == 0:
        limit = None
        offset = None
    else:
        limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''

    # 获取筛选参数
    navStatus = request.POST.get('navStatus',"").strip()


    # 全部学生信息里面包含搜索条件
    if navStatus == 'all':
        listStudentInfo = student.objects.filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search)|Q(person__contains=search))\
                           .order_by('-create_time')[offset:limit]\
            .values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'school_car', 'is_shuangliu', 'is_chengdu', 'infos', 'address', 'person', 'remark')
        StudentInfoCount = student.objects.filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search)|Q(person__contains=search)).count()
    else:
        listStudentInfo = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search)|Q(person__contains=search))\
                                                                         .order_by('-create_time')[offset:limit].\
            values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'school_car', 'is_shuangliu', 'is_chengdu', 'infos', 'address', 'person', 'remark')
        StudentInfoCount = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search)|Q(person__contains=search)).count()

    # QuerySet 序列化
    rows = [row for row in listStudentInfo]

    result = {"total": StudentInfoCount, "rows": rows}
    # 返回查询结果
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


# 获取流水信息列表
@csrf_exempt
def getmoneyflow(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)

    limit = int(request.POST.get('limit', 0))
    offset = int(request.POST.get('offset', 0))
    if limit == 0 and offset == 0:
        limit = None
        offset = None
    else:
        limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''

    # 获取筛选参数
    # navStatus = request.POST.get('navStatus',"").strip()


    # 全部学生信息里面包含搜索条件
    listStudentInfo = Flowing.objects.filter(Q(stuId__name__contains=search)|Q(type=search)|Q(action=search)|Q(person__contains=search))\
                                                                     .order_by('-create_time')[offset:limit].\
        values("id", 'stuId__name', 'action', 'type', 'flowing', 'create_time', 'person', 'remark')
    StudentInfoCount = Flowing.objects.filter(Q(stuId__name__contains=search)|Q(type=search)|Q(action=search)|Q(person__contains=search)).count()

    # QuerySet 序列化
    rows = [row for row in listStudentInfo]

    result = {"total": StudentInfoCount, "rows": rows}
    # 返回查询结果
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


# 获取预收费信息列表
@csrf_exempt
def getpremoney(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)

    limit = int(request.POST.get('limit', 0))
    offset = int(request.POST.get('offset', 0))
    if limit == 0 and offset == 0:
        limit = None
        offset = None
    else:
        limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''

    # 获取筛选参数
    navStatus = request.POST.get('navStatus',"").strip()


    # 全部学生信息里面包含搜索条件
    if navStatus == 'all':
        listStudentInfo = student.objects.filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(pre_person__contains=search))\
                           .order_by('-create_time')[offset:limit]\
            .values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'pre_person', 'premoney')
        StudentInfoCount = student.objects.filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(pre_person__contains=search)).count()
    else:
        listStudentInfo = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(pre_person__contains=search))\
                                                                         .order_by('-create_time')[offset:limit].\
            values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'pre_person', 'premoney')
        StudentInfoCount = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(pre_person__contains=search)).count()

    # QuerySet 序列化
    rows = [row for row in listStudentInfo]

    result = {"total": StudentInfoCount, "rows": rows}
    # 返回查询结果
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


# 获取学生报名信息列表
@csrf_exempt
def getregister(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)

    limit = int(request.POST.get('limit', 0))
    offset = int(request.POST.get('offset', 0))
    if limit == 0 and offset == 0:
        limit = None
        offset = None
    else:
        limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''
    # 获取筛选参数
    sel_term = int(request.POST.get('sel_term', "").strip())
    sel_class = request.POST.get('sel_class', "").strip()
    sel_register = request.POST.get('sel_register', "").strip()


    # 全部学生信息里面包含搜索条件
    listStudentInfo = student.objects.filter(Q(classid__class_name__contains=sel_class)).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search))\
                           .order_by('-create_time')[offset:limit]\
            .values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'school_car', 'is_shuangliu', 'is_chengdu', 'infos', 'address')
    StudentInfoCount = student.objects.filter(Q(classid__class_name__contains=sel_class)).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)).count()

    # QuerySet 序列化
    rows_all = []
    rows_register = []
    rows_unregister = []
    for row in listStudentInfo:
        tmp = row.copy()
        stuid = row["id"]
        listStuTermInfo = student_term_info.objects.filter(stuId=stuid, termId__id=sel_term).values("status")
        if listStuTermInfo:
            tmp["status"] = listStuTermInfo[0]["status"]
            rows_register.append(tmp)
        else:
            tmp["status"] = ""
            rows_unregister.append(tmp)
        rows_all.append(tmp)

    if sel_register == "all":
        rows = rows_all
    elif sel_register == "已报到":
        rows = rows_register
    elif sel_register == "未报到":
        rows = rows_unregister
    else:
        rows = []

    result = {"total": StudentInfoCount, "rows": rows}
    # 返回查询结果
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


# 获取学生缴费信息列表
@csrf_exempt
def getmoneysinfo(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)

    limit = int(request.POST.get('limit', 0))
    offset = int(request.POST.get('offset', 0))
    if limit == 0 and offset == 0:
        limit = None
        offset = None
    else:
        limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''

    # 获取筛选参数
    sel_term = request.POST.get('sel_term', "").strip()
    sel_class = request.POST.get('sel_class', "").strip()
    sel_type = request.POST.get('sel_type', "").strip()
    sel_action = request.POST.get('sel_action', "").strip()
    sel_status = request.POST.get('sel_status', "").strip()

    # 全部学生缴费信息里面包含搜索条件
    listMoneyInfo = PayMentInfo.objects.filter(termId__id=sel_term)\
        .filter(Q(stuId__classid__class_name__contains=sel_class) & Q(type__contains=sel_type) & Q(action__contains=sel_action) & Q(status__contains=sel_status))\
        .filter(Q(stuId__name__contains=search) | Q(money__contains=search) |Q(person__contains=search))\
        .order_by('-create_time')[offset:limit]\
        .values("id", "stuId__name", "stuId__classid__class_name", "type", 'action', 'money', 'status', 'person', 'remark')

    MoneyInfoCount = PayMentInfo.objects.filter(termId__id=sel_term) \
        .filter(Q(stuId__classid__class_name__contains=sel_class) & Q(type__contains=sel_type) & Q(
        action__contains=sel_action) & Q(status__contains=sel_status)) \
        .filter(Q(stuId__name__contains=search) | Q(money__contains=search) | Q(person__contains=search)).count()

    # QuerySet 序列化
    rows = [row for row in listMoneyInfo]

    result = {"total": MoneyInfoCount, "rows": rows}
    # 返回查询结果
    return HttpResponse(json.dumps(result, cls=ExtendJSONEncoder, bigint_as_string=True),
                        content_type='application/json')


# 删除学生信息
@csrf_exempt
def delstudent(request):
    students = request.POST.get('studentsInfo', "")
    result = {'status': 0, 'msg': '删除学生信息成功！', 'data': []}

    if not students:
        result['status'] = 1
        result['msg'] = '请选择需要删除信息的学生！'
        return HttpResponse(json.dumps(result), content_type='application/json')

    student_ids = students.split("&")
    # 使用事务保持数据一致性
    try:
        with transaction.atomic():
            for student_id in student_ids:
                id = int(student_id.split("=")[1])
                student.objects.get(id=id).delete()
    except Exception as msg:
        import traceback
        print(traceback.format_exc())
        result['status'] = 1
        result['msg'] = str(msg)
        return HttpResponse(json.dumps(result), content_type='application/json')

    return HttpResponse(json.dumps(result), content_type='application/json')

# 修改预收费
@csrf_exempt
def modifypremoney(request):
    # 获取用户信息
    loginUser = request.session.get('login_username', False)
    students = request.POST.get('studentsInfo', "")
    msg = request.POST.get('msg', '')
    result = {'status': 0, 'msg': '修改预收费成功！', 'data': []}

    loginUserOb = users.objects.get(username=loginUser)
    UserDisplay = loginUserOb.display

    if not students:
        result['status'] = 1
        result['msg'] = '请选择需要修改预收费的学生！'
        return HttpResponse(json.dumps(result), content_type='application/json')

    student_ids = students.split("&")

    if len(student_ids) != 1:
        result['status'] = 1
        result['msg'] = '一次只能修改一个学生！'
        return HttpResponse(json.dumps(result), content_type='application/json')

    try:
        msg = float(msg)
    except Exception as e:
        result['status'] = 1
        result['msg'] = '输入的金额不正确！'
        return HttpResponse(json.dumps(result), content_type='application/json')

    # 使用事务保持数据一致性
    try:
        with transaction.atomic():
            for student_id in student_ids:
                id = int(student_id.split("=")[1])
                stuinfo = student.objects.get(id=id)
                try:
                    l_premoney = float(stuinfo.premoney)
                except Exception as e:
                    l_premoney = 0.0
                flowing = msg - l_premoney 
                stuinfo.premoney = msg
                stuinfo.pre_person = UserDisplay
                stuinfo.save()
                if flowing > 0:
                    f_type = "收款"
                elif flowing < 0:
                    f_type = "退款"
                else:
                    f_type = "无需缴费"
                if f_type != "无需缴费":
                    Flowing.objects.create(stuId=stuinfo, action="现金", type=f_type, flowing=flowing, person=UserDisplay)
    except Exception as msg:
        import traceback
        print(traceback.format_exc())
        result['status'] = 1
        result['msg'] = str(msg)
        return HttpResponse(json.dumps(result), content_type='application/json')

    return HttpResponse(json.dumps(result), content_type='application/json')


# 提交学生信息到数据库
@csrf_exempt
def addstutodb(request):
    id = request.POST.get('id', '').strip()
    # 获取用户信息
    loginUser = request.session.get('login_username', False)
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
    result = {'status': 0, 'msg': '添加学生信息成功！', 'data': ""}

    loginUserOb = users.objects.get(username=loginUser)
    UserDisplay = loginUserOb.display

    if len(tel_num) != 11:
        result['status'] = 1
        result['msg'] = '联系电话输入不正确!'
        return HttpResponse(json.dumps(result), content_type='application/json')

    try:
        if id:
            Student = student.objects.get(id=id)
            Student.name = name
            Student.tel_num = tel_num
            Student.card_id = card_id
            Student.birthday = birthday
            Student.classid_id = classid
            Student.sex = sex
            Student.fa_name = fa_name
            Student.school_car = school_car
            Student.is_shuangliu = is_shuangliu
            Student.is_chengdu = is_chengdu
            Student.infos = infos
            Student.address = address
            Student.person = UserDisplay
            Student.remark = remark
            Student.save()
            result["msg"] = "编辑学生信息成功!"
        else:
            # if student.objects.filter(card_id=card_id):
            #     result['status'] = 1
            #     result['msg'] = '该身份证号码的学生已存在!'
            #     return HttpResponse(json.dumps(result), content_type='application/json')
            Student = student(name=name,tel_num=tel_num, card_id=card_id, birthday=birthday, classid_id=classid, sex=sex, fa_name=fa_name,
                school_car=school_car, is_shuangliu=is_shuangliu, is_chengdu=is_chengdu, infos=infos, address=address, person=UserDisplay, remark=remark)
            Student.save()
            id = student.objects.all()[0].id
    except Exception as msg:
        import traceback
        print(traceback.format_exc())
        result['status'] = 1
        if id:
            result['msg'] = '编辑学生信息失败，请联系管理员处理!'
        else:
            result['msg'] = '添加学生信息失败，请联系管理员处理!'
        return HttpResponse(json.dumps(result), content_type='application/json')
    result['data'] = {"stuid": str(id)}
    result['data']['termid'] = TermInfo.objects.filter()[0].id
    return HttpResponse(json.dumps(result), content_type='application/json')


# 查询应缴费用/生成发票/生成二维码
@csrf_exempt
def seladdmoney(request):
    # 查询应缴费信息
    loginUser = request.session.get('login_username', False)
    stuId = request.POST.get('stuId', '').strip()
    termId = request.POST.get('termId', '').strip()
    index = request.POST.get('index', '').strip()
    remark = request.POST.get('remark', '').strip()
    payMents = []
    for i in range(1, int(index) + 1):
        payMents.append(request.POST.get("f_id_" + str(i), '').strip())
    print(payMents)
    pay_money = []
    for pay_ment in payMents:
        f_type, f_aciton, f_money = pay_ment.split("_")
        f_money = float(f_money)
        MoneyInfo = PayMentInfo.objects.filter(stuId__id=stuId, termId__id=termId, type=f_type, action=f_aciton)
        if MoneyInfo:
            money_inc = f_money - MoneyInfo[0].money
        else:
            money_inc = f_money
        pay_money.append((f_type, f_aciton, money_inc))
    print(pay_money)
    result = {'status': 0, 'msg': '学生缴费成功！', 'data': ""}
    return HttpResponse(json.dumps(result), content_type='application/json')


# 提交缴费信息到数据库
@csrf_exempt
def addmoneytodb(request):
    # 缴费信息
    loginUser = request.session.get('login_username', False)
    stuId = request.POST.get('stuId', '').strip()
    termId = request.POST.get('termId', '').strip()
    index = request.POST.get('index', '').strip()
    remark = request.POST.get('remark', '').strip()

    loginUserOb = users.objects.get(username=loginUser)
    UserDisplay = loginUserOb.display

    payMents = []
    for i in range(1, int(index) + 1):
        payMents.append(request.POST.get("f_id_" + str(i), '').strip())
    stuObj = get_object_or_404(student, id=stuId)
    termObj = get_object_or_404(TermInfo, id=termId)
    pay_money = []
    try:
        with transaction.atomic():
            term_flag = 0
            for pay_ment in payMents:
                f_type, f_aciton, f_money = pay_ment.split("_")
                f_money = float(f_money)
                if f_money == 0:
                    f_status = "未缴费"
                else:
                    term_flag = 1
                    f_status = "已缴费"
                MoneyInfo, flag = PayMentInfo.objects.get_or_create(stuId=stuObj, termId=termObj, type=f_type, action=f_aciton)
                if flag:
                    money_inc = f_money
                else:
                    money_inc = f_money - MoneyInfo.money
                MoneyInfo.money = f_money
                MoneyInfo.status = f_status
                MoneyInfo.remark = remark
                MoneyInfo.person = UserDisplay
                MoneyInfo.save()
                pay_money.append((f_type, f_aciton, money_inc))
            stu_term_info, flag = student_term_info.objects.get_or_create(stuId=stuObj, termId=termObj)
            if term_flag:
                stu_term_info.status = "已报到"
                stu_term_info.save()
            else:
                stu_term_info.delete()

            all_money = sum([i[2] for i in pay_money])
            stu_pre_money = stuObj.premoney
            flowing = all_money - stu_pre_money
            if flowing > 0:
                f_type = "收款"
            elif flowing < 0:
                f_type = "退款"
            else:
                f_type = "无需缴费"
            if f_type != "无需缴费":
                Flowing.objects.create(stuId=stuObj, action="现金", type=f_type, flowing=flowing, person=UserDisplay)

            stuObj.premoney = 0
            stuObj.save()

    except Exception as e:
        print(traceback.format_exc())
        result = {'status': 1, 'msg': '学生缴费信息写入数据库失败，请联系管理员！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')

    msg = f"""学生缴费成功！
    应缴费用:{all_money},
    抵扣预收费:{stu_pre_money},
    实际缴费:{flowing}
    """

    result = {'status': 0, 'msg': msg, 'data': ""}

    return HttpResponse(json.dumps(result), content_type='application/json')


#上传文件
@csrf_exempt
def upload(request):
    myFile = request.FILES['file_data']
    upload_path = settings.UPLOAD_PATH
    if not myFile:
        return HttpResponse("no files for upload!")
    try:
        clear(upload_path)
        destination = open(os.path.join(upload_path, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
            destination.close()
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return HttpResponse("upload failed!")
    result = {'status': 0, 'msg': '文件上传成功！', 'data': []}
    return HttpResponse(json.dumps(result), content_type='application/json')


#导入excel
@csrf_exempt
def importexcel(request):
    """
    新建 Microsoft Excel 工作表.xlsx all Done
    :param request:
    :return:
    """
    filename = request.POST.get("filename", "").strip()
    type = request.POST.get("type", "").strip()
    process = request.POST.get("process", "").strip()
    result = {'status': 0, 'msg': '学生信息导入成功！', 'data': []}
    if not filename:
        result = {'status': 1, 'msg': '请选择需要导入的文件！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')
    if not (filename.endswith(".xls") or filename.endswith(".xlsx")):
        result = {'status': 1, 'msg': '请使用模板文件文件导入！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')
    if process != "Done":
        result = {'status': 1, 'msg': '请上传需要导入的文件！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')

    class_dict = {class_i.class_name: class_i.id for class_i in classes.objects.all()}

    try:
        import_file = os.path.join(settings.UPLOAD_PATH, filename)
        df = pd.read_excel(import_file)
        df = df[settings.HEAD_LIST]
        df = df.fillna("")
        df[["身份证号码", "联系电话"]] = df[["身份证号码", "联系电话"]].applymap(str)
        df[["班级"]] = df[["班级"]].applymap(class_dict.get)
        fun = lambda datastr: datetime.datetime.strptime(datastr, '%Y-%m-%d')
        df[["出生年月"]] = df[["出生年月"]].applymap(fun)
    except Exception as e:
        print(traceback.format_exc())
        result = {'status': 1, 'msg': '上传的文件有误，请仔细确认！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')
    try:
        with transaction.atomic():
            if type == "all":
                student.objects.all().delete()
            for i in range(len(df)):
                df_i = df.iloc[i]
                student.objects.get_or_create(name=df_i["姓名"], tel_num=df_i["联系电话"], card_id=df_i["身份证号码"],
                                              birthday=df_i["出生年月"], classid_id=df_i["班级"], sex=df_i["性别"],
                                              fa_name=df_i["监护人姓名"], school_car=df_i["校车"], is_shuangliu=df_i["是否双流户籍"],
                                              is_chengdu=df_i["是否大成都"], infos=df_i["材料"], address=df_i["户籍详细地址"],
                                              remark=df_i["备注"])
    except Exception as e:
        print(traceback.format_exc())
        result = {'status': 1, 'msg': '学生信息导入数据库有误，请联系管理员！', 'data': []}
        return HttpResponse(json.dumps(result), content_type='application/json')

    return HttpResponse(json.dumps(result), content_type='application/json')


if __name__ == "__main__":
    pass
