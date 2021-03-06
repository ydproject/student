# -*- coding: UTF-8 -*-
"""
Django settings for student project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n($+xivz(je4037%+)0-20x#=q(ma#u8sp*++(ve^keh@0qz)c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'stuMgr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'stuMgr.check_login_middleware.CheckLoginMiddleware',
    'stuMgr.exception_logging_middleware.ExceptionLoggingMiddleware',
)

ROOT_URLCONF = 'student.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'stuMgr/static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'stuMgr.processor.global_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'student.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# 时间格式化
USE_L10N = False
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = "stuMgr.users"


# session 设置
SESSION_COOKIE_AGE = 60 * 30  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

stamdard_format = '[%(asctime)s][%(threadName)s:%(thread)d]' + \
                  '[task_id:%(name)s][%(filename)s:%(lineno)d] ' + \
                  '[%(levelname)s]- %(message)s'

DEFAULT_LOGS = os.path.join(BASE_DIR, 'default.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {  # 详细
            'format': stamdard_format
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DEFAULT_LOGS,
            'maxBytes': 1024 * 1024 * 100,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'default': {  # default日志，存放于log中
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        # 'django.db': {  # 打印SQL语句到console，方便开发
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        'django.request': {  # 打印错误堆栈信息到console，方便开发
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# 账户登录失败锁定时间(秒)
LOCK_TIME_THRESHOLD = 300
# 账户登录失败 几次 锁账户
LOCK_CNT_THRESHOLD = 5

# 用户上传文件的目录
UPLOAD_PATH = os.path.join(BASE_DIR, "upload")

# STUDENT EXCEL HEAD LIST
HEAD_LIST = ['姓名', '联系电话', '身份证号码', '出生年月', '班级', '性别', '监护人姓名', '校车', '是否双流户籍', '是否大成都', '材料', '户籍详细地址', '备注']