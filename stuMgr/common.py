#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: yuandi
@contact: 675041110@qq.com
@file: common.py
@time: 2018/9/28 23:47
"""

import os
import shutil

from .models import PayMentInfo


def clear(path):
    shutil.rmtree(path)
    os.mkdir(path)


def get_money_info():
    pass


if __name__ == "__main__":
    pass
