# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 角色分两种：
# 1.教师：可以提交学生信息的教师们，username字段为登录用户名，display字段为展示的中文名。
# 2.财务：可以提交学生信息和缴费信息的人员们。
class users(AbstractUser):
    display = models.CharField('显示的中文名', max_length=50)
    role = models.CharField('角色', max_length=20, choices=(('教师', '教师'), ('财务', '财务'), ('管理员', '管理员')), default='教师')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = u'用户配置'
        verbose_name_plural = u'用户配置'


class classes(models.Model):
    class_name = models.CharField('班级', max_length=50)
    teacher_name = models.CharField('老师姓名', max_length=50)
    class_rom = models.CharField('教室编号', max_length=50)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = u'班级配置'
        verbose_name_plural = u'班级配置'
        ordering = ["-id"]


class student(models.Model):
    name = models.CharField('姓名', max_length=50)
    tel_num = models.CharField('联系电话', max_length=50)
    card_id = models.CharField('身份证件号码', max_length=50)
    birthday = models.DateField('出生年月',null=True, blank=True)
    classid = models.ForeignKey(classes, verbose_name='班级')
    sex = models.CharField('性别', choices=(('男', '男'), ('女', '女')), max_length=20)
    fa_name = models.CharField('监护人姓名', max_length=50)
    school_car = models.CharField('校车', max_length=50)
    is_shuangliu = models.CharField('是否双流户籍', choices=(('否', '否'), ('是', '是')), max_length=20)
    is_chengdu = models.CharField('是否大成都', choices=(('否', '否'), ('是', '是')), max_length=20)
    infos = models.CharField('材料', max_length=50)
    address = models.CharField('户籍详细地址', max_length=180)
    remark = models.TextField('备注')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'学生信息'
        verbose_name_plural = u'学生信息'
        ordering = ["-id"]


class TermInfo(models.Model):
    term_name = models.CharField(max_length=20, verbose_name=u"名称")

    def __str__(self):
        return self.term_name

    class Meta:
        verbose_name = u'学期'
        verbose_name_plural = u'学期'
        ordering = ["-id"]


class student_term_info(models.Model):
    stuId = models.ForeignKey('student', to_field='id', verbose_name='学号')
    termId = models.ForeignKey('TermInfo', to_field='id', verbose_name=u"学期")
    status = models.CharField(max_length=20, verbose_name=u"报名情况", choices=(('已报到', '已报到'), ('未报到', '未报到')),
                              default="未报到")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return str(self.stuId) + "_" + self.termId

    class Meta:
        verbose_name = u'学生报名信息'
        verbose_name_plural = u'学生报名信息'
        ordering = ["-id"]


class Payment_item(models.Model):
    audit_id = models.AutoField(primary_key=True)
    type_info = models.CharField(max_length=20, verbose_name=u"种类")
    action = models.CharField(max_length=20, choices=(
        ('All', 'All'), ('1月', '1月'), ('2月', '2月'), ('3月', '3月'), ('4月', '4月'),('5月', '5月'),
        ('6月', '6月'), ('7月', '7月'), ('8月', '8月'), ('9月', '9月'), ('10月', '10月'), ('11月', '11月'),
        ('12月', '12月')), verbose_name="费用期间", default="All")
    money = models.CharField(max_length=20, verbose_name=u"金额")


    def __str__(self):
        return str(self.audit_id) + "_" + self.type_info + "_" + self.action + "_" + self.money

    class Meta:
        verbose_name = u'缴费种类'
        verbose_name_plural = u'缴费种类'
        ordering = ["-audit_id"]


class Payment_Plan(models.Model):
    audit_id = models.AutoField(primary_key=True)
    plan = models.ManyToManyField(Payment_item, verbose_name=u"缴费计划")

    class Meta:
        verbose_name = u'缴费计划'
        verbose_name_plural = u'缴费计划'
        ordering = ["-audit_id"]


class PayMentInfo(models.Model):
    stuId = models.ForeignKey('student', to_field='id', verbose_name='学号')
    termId = models.ForeignKey('TermInfo', to_field='id', verbose_name=u"学期")
    type = models.CharField(max_length=20, verbose_name=u"种类")
    action = models.CharField(max_length=20, verbose_name=u"费用期间")
    money = models.FloatField(default=0.0, verbose_name=u"金额")
    status = models.CharField(max_length=20, verbose_name=u"缴费情况")
    remark = models.TextField(max_length=20, verbose_name=u"备注")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = u"缴费信息"
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class PreMent(models.Model):
    stuId = models.ForeignKey('student', to_field='id', verbose_name='学号')
    premoney = models.FloatField(default=0.0, verbose_name=u"预收费")
    remark = models.TextField(max_length=20, verbose_name=u"备注")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = u"预收费信息"
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class Flowing(models.Model):
    stuId = models.ForeignKey('student', to_field='id', verbose_name='学号')
    flowing = models.FloatField(default=0.0, verbose_name=u"金额")
    remark = models.TextField(max_length=20, verbose_name=u"备注")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = u"流水信息"
        verbose_name_plural = verbose_name
        ordering = ["-id"]