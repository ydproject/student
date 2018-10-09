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
from django.db.models import Q
from django.db import transaction
import pandas as pd

from .extend_json_encoder import ExtendJSONEncoder
from .models import student, classes
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

    limit = int(request.POST.get('limit'))
    offset = int(request.POST.get('offset'))
    limit = offset + limit

    # 获取搜索参数
    search = request.POST.get('search',"").strip()
    if search is None:
        search = ''

    # 获取筛选参数
    navStatus = request.POST.get('navStatus',"").strip()


    # 全部学生信息里面包含搜索条件
    if navStatus == 'all':
        listStudentInfo = student.objects.filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search))\
                           .order_by('-create_time')[offset:limit]\
            .values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'school_car', 'is_shuangliu', 'is_chengdu', 'infos', 'address', 'remark')
        StudentInfoCount = student.objects.filter().count()
    else:
        listStudentInfo = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search))\
                                                                         .order_by('-create_time')[offset:limit].\
            values("id", 'name', 'tel_num', 'card_id', 'birthday', 'classid__class_name', 'sex',
                   'fa_name', 'school_car', 'is_shuangliu', 'is_chengdu', 'infos', 'address', 'remark')
        StudentInfoCount = student.objects.filter(classid__id=navStatus).filter(Q(name__contains=search)|Q(tel_num__contains=search)|Q(card_id__contains=search)|Q(sex=search)|Q(fa_name__contains=search)|Q(address__contains=search)).count()

    # QuerySet 序列化
    rows = [row for row in listStudentInfo]

    result = {"total": StudentInfoCount, "rows": rows}
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


# 提交学生信息到数据库
@csrf_exempt
def addstutodb(request):
    id = request.POST.get('id', '').strip()
    print(id)
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
    result = {'status': 0, 'msg': '添加学生信息成功！', 'data': []}

    if len(tel_num) != 11:
        result['status'] = 1
        result['msg'] = '联系电话输入不正确!'
        return HttpResponse(json.dumps(result), content_type='application/json')
    if len(card_id) != 18:
        result['status'] = 1
        result['msg'] = '身份证号码输入不正确!'
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
            Student.remark = remark
            Student.save()
            result["msg"] = "编辑学生信息成功!"
        else:
            if student.objects.filter(card_id=card_id):
                result['status'] = 1
                result['msg'] = '该身份证号码的学生已存在!'
                return HttpResponse(json.dumps(result), content_type='application/json')
            Student = student(name=name,tel_num=tel_num, card_id=card_id, birthday=birthday, classid_id=classid, sex=sex, fa_name=fa_name,
                school_car=school_car, is_shuangliu=is_shuangliu, is_chengdu=is_chengdu, infos=infos, address=address, remark=remark)
            Student.save()
    except Exception as msg:
        import traceback
        print(traceback.format_exc())
        result['status'] = 1
        if id:
            result['msg'] = '编辑学生信息失败，请联系管理员处理!'
        else:
            result['msg'] = '添加学生信息失败，请联系管理员处理!'
        return HttpResponse(json.dumps(result), content_type='application/json')

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
    print("********", process, type, filename)
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
                print(df_i)
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
