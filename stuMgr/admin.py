# -*- coding: UTF-8 -*- 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from .models import users, classes, student, Payment_Plan, Payment_item, PayMentInfo, PreMent, Flowing, TermInfo


@admin.register(users)
class usersAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('id', 'username', 'display', 'role', 'email', 'is_superuser', 'is_staff', 'is_active')
        self.search_fields = ('id', 'username', 'display', 'role', 'email')


@admin.register(TermInfo)
class TermInfoAdmin(admin.ModelAdmin):
    list_display = ('term_name',)
    search_fields = ['term_name',]


@admin.register(classes)
class classesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'teacher_name', 'class_rom')
    search_fields = ['class_name', 'teacher_name', 'class_rom']


@admin.register(student)
class studentAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel_num', 'card_id', 'birthday', 'classid', 'sex', 'fa_name', 'school_car',
                    'is_shuangliu', 'is_chengdu', 'infos', 'address', 'remark')
    search_fields = ['name', 'tel_num', 'card_id', 'birthday', 'classid', 'sex', 'fa_name', 'school_car',
                    'is_shuangliu', 'is_chengdu', 'infos', 'address', 'remark']


admin.site.register(Payment_Plan)


@admin.register(Payment_item)
class Payment_itemAdmin(admin.ModelAdmin):
    list_display = ('type_info', 'action', 'money')
    search_fields = ['type_info', 'action', 'money']


@admin.register(PayMentInfo)
class PayMentInfoAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'termId', 'type', 'action', 'money', 'status', 'remark')
    search_fields = ['stuId', 'termId', 'type', 'action', 'money', 'status', 'remark']


@admin.register(PreMent)
class PreMentAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'premoney', 'remark')
    search_fields = ['stuId', 'premoney', 'remark']


@admin.register(Flowing)
class FlowingAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'flowing', 'remark')
    search_fields = ['stuId', 'flowing', 'remark']