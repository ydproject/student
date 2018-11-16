# -*- coding: UTF-8 -*- 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from .models import users, classes, student, Payment_Plan, Payment_item, PayMentInfo, PreMent, Flowing, TermInfo, student_term_info


@admin.register(users)
class usersAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('id', 'username', 'display', 'role', 'email', 'is_superuser', 'is_staff', 'is_active')
        self.search_fields = ('id', 'username', 'display', 'role', 'email')

        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

    def changelist_view(self, request, extra_context=None):
        # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
        if request.user.is_superuser:
            # 此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
            self.fieldsets = (
                (('认证信息'), {'fields': ('username', 'password')}),
                (('个人信息'), {'fields': ('display', 'role', 'email')}),
                (('权限信息'), {'fields': ('is_active', 'is_staff')}),
                # (('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
            # 此字段定义UserCreationForm表单中的具体显示内容
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'display', 'role', 'email', 'password1', 'password2'),
                                          }),
                                  )
        return super(UserAdmin, self).changelist_view(request, extra_context)


@admin.register(TermInfo)
class TermInfoAdmin(admin.ModelAdmin):
    list_display = ('term_name',)
    search_fields = ['term_name',]


@admin.register(classes)
class classesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'teacher_name', 'class_rom')
    search_fields = ['class_name', 'teacher_name', 'class_rom']


@admin.register(student_term_info)
class StudentTermAdmin(admin.ModelAdmin):
    list_display = ('stuId', 'termId', 'status')
    search_fields = ['stuId', 'termId', 'status']


@admin.register(student)
class studentAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel_num', 'card_id', 'birthday', 'classid', 'sex', 'fa_name', 'school_car',
                    'is_shuangliu', 'is_chengdu', 'infos', 'address', 'person', 'remark')
    search_fields = ['name', 'tel_num', 'card_id', 'birthday', 'classid', 'sex', 'fa_name', 'school_car',
                    'is_shuangliu', 'is_chengdu', 'infos', 'address', 'person', 'remark']


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