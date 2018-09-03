#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: yuandi
@file: view_ajax.py
@time: 2018/9/3 21:49
"""

import datetime
import simplejson as json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate


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


if __name__ == "__main__":
    pass
