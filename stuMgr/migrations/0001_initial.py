# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('display', models.CharField(verbose_name='显示的中文名', max_length=50)),
                ('role', models.CharField(verbose_name='角色', max_length=20, default='教师', choices=[('教师', '教师'), ('财务', '财务'), ('管理员', '管理员')])),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户配置',
                'verbose_name_plural': '用户配置',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='classes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_name', models.CharField(verbose_name='班级', max_length=50)),
                ('teacher_name', models.CharField(verbose_name='老师姓名', max_length=50)),
                ('class_rom', models.CharField(verbose_name='教室编号', max_length=50)),
            ],
            options={
                'verbose_name': '班级配置',
                'verbose_name_plural': '班级配置',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Flowing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('flowing', models.CharField(verbose_name='金额', max_length=20)),
                ('action', models.CharField(verbose_name='操作', max_length=20)),
                ('time', models.CharField(verbose_name='时间', max_length=20)),
                ('remark', models.TextField(verbose_name='备注', max_length=20)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '预收费信息',
                'verbose_name_plural': '预收费信息',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Payment_item',
            fields=[
                ('audit_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_info', models.CharField(verbose_name='种类', max_length=20)),
                ('action', models.CharField(verbose_name='费用期间', max_length=20, default='All', choices=[('All', 'All'), ('1月', '1月'), ('2月', '2月'), ('3月', '3月'), ('4月', '4月'), ('5月', '5月'), ('6月', '6月'), ('7月', '7月'), ('8月', '8月'), ('9月', '9月'), ('10月', '10月'), ('11月', '11月'), ('12月', '12月')])),
                ('money', models.CharField(verbose_name='金额', max_length=20)),
            ],
            options={
                'verbose_name': '缴费种类',
                'verbose_name_plural': '缴费种类',
                'ordering': ['-audit_id'],
            },
        ),
        migrations.CreateModel(
            name='Payment_Plan',
            fields=[
                ('audit_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan', models.ManyToManyField(verbose_name='缴费计划', to='stuMgr.Payment_item')),
            ],
            options={
                'verbose_name': '缴费计划',
                'verbose_name_plural': '缴费计划',
                'ordering': ['-audit_id'],
            },
        ),
        migrations.CreateModel(
            name='PayMentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('termId', models.CharField(verbose_name='学期', max_length=20)),
                ('type', models.CharField(verbose_name='种类', max_length=20)),
                ('action', models.CharField(verbose_name='费用期间', max_length=20)),
                ('money', models.CharField(verbose_name='金额', max_length=20)),
                ('status', models.CharField(verbose_name='缴费情况', max_length=20)),
                ('remark', models.TextField(verbose_name='备注', max_length=20)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '缴费信息',
                'verbose_name_plural': '缴费信息',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PreMent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('premoney', models.CharField(verbose_name='预收费', max_length=20)),
                ('remark', models.TextField(verbose_name='备注', max_length=20)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '预收费信息',
                'verbose_name_plural': '预收费信息',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=50)),
                ('tel_num', models.CharField(verbose_name='联系电话', max_length=50)),
                ('card_id', models.CharField(verbose_name='身份证件号码', max_length=50)),
                ('birthday', models.DateField(verbose_name='出生年月', blank=True, null=True)),
                ('sex', models.CharField(verbose_name='性别', max_length=20, choices=[('男', '男'), ('女', '女')])),
                ('fa_name', models.CharField(verbose_name='监护人姓名', max_length=50)),
                ('school_car', models.CharField(verbose_name='校车', max_length=50)),
                ('is_shuangliu', models.CharField(verbose_name='是否双流户籍', max_length=20, choices=[('否', '否'), ('是', '是')])),
                ('is_chengdu', models.CharField(verbose_name='是否大成都', max_length=20, choices=[('否', '否'), ('是', '是')])),
                ('infos', models.CharField(verbose_name='材料', max_length=50)),
                ('address', models.CharField(verbose_name='户籍详细地址', max_length=180)),
                ('remark', models.TextField(verbose_name='备注')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('class_id', models.ForeignKey(verbose_name='班级', default=1, to='stuMgr.classes')),
            ],
            options={
                'verbose_name': '学生信息',
                'verbose_name_plural': '学生信息',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='prement',
            name='stuId',
            field=models.ForeignKey(verbose_name='学号', to='stuMgr.student'),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='stuId',
            field=models.ForeignKey(verbose_name='学号', to='stuMgr.student'),
        ),
        migrations.AddField(
            model_name='flowing',
            name='stuId',
            field=models.ForeignKey(verbose_name='学号', to='stuMgr.student'),
        ),
    ]
