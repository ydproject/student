# -*- coding: UTF-8 -*-
from .models import users
from django.conf import settings

leftMenuBtnsCommon = (
    {'key': 'studentsinfo', 'name': '学生基本信息', 'url': '/studentsinfo/', 'class': 'glyphicon glyphicon-home',
     'display': True},
    {'key': 'register', 'name': '学生报名/缴费', 'url': '/register/', 'class': 'glyphicon glyphicon-align-right',
     'display': True},
    {'key': 'premoney', 'name': '学生预收费', 'url': '/premoney/', 'class': 'glyphicon glyphicon-scissors',
     'display': True},
    {'key': 'moneysinfo', 'name': '缴费明细信息', 'url': '/moneysinfo/', 'class': 'glyphicon glyphicon-eye-open',
     'display': True},
    {'key': 'moneyflow', 'name': '缴费流水信息', 'url': '/moneyflow/', 'class': 'glyphicon glyphicon-wrench',
     'display': True},
)

leftMenuBtnsSuper = (
    {'key': 'admin', 'name': '后台数据管理', 'url': '/admin/stuMgr/', 'class': 'glyphicon glyphicon-list', 'display': True},
)

leftMenuBtnsDoc = (
    {'key': 'charts', 'name': '统计图表展示', 'url': '/charts/', 'class': 'glyphicon glyphicon-file', 'display': True},
)


def global_info(request):
    """存放用户，会话信息等."""
    loginUser = request.session.get('login_username', None)
    if loginUser is not None:
        user = users.objects.get(username=loginUser)
        UserDisplay = user.display
        if UserDisplay == '':
            UserDisplay = loginUser
        if user.is_superuser:
            leftMenuBtns = leftMenuBtnsCommon + leftMenuBtnsSuper + leftMenuBtnsDoc
        else:
            leftMenuBtns = leftMenuBtnsCommon
    else:
        leftMenuBtns = ()
        UserDisplay = ''

    return {
        'loginUser': loginUser,
        'leftMenuBtns': leftMenuBtns,
        'UserDisplay': UserDisplay,
    }
