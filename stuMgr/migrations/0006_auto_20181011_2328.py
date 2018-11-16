# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0005_auto_20180903_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='student_term_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.CharField(verbose_name='报名情况', max_length=20, default='未报到', choices=[('已报到', '已报到'), ('未报到', '未报到')])),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '学生报名信息',
                'verbose_name_plural': '学生报名信息',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelOptions(
            name='flowing',
            options={'verbose_name': '流水信息', 'verbose_name_plural': '流水信息', 'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='payment_item',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='class_id',
        ),
        migrations.AddField(
            model_name='student',
            name='classid',
            field=models.ForeignKey(verbose_name='班级', default=2, to='stuMgr.classes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_term_info',
            name='stuId',
            field=models.ForeignKey(verbose_name='学号', to='stuMgr.student'),
        ),
        migrations.AddField(
            model_name='student_term_info',
            name='termId',
            field=models.ForeignKey(verbose_name='学期', to='stuMgr.TermInfo'),
        ),
    ]
