# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0011_auto_20181018_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinfo',
            name='remark',
            field=models.TextField(verbose_name='备注', max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='remark',
            field=models.TextField(verbose_name='备注', default=''),
        ),
        migrations.AlterField(
            model_name='student_term_info',
            name='status',
            field=models.CharField(verbose_name='报名情况', max_length=20, default='', choices=[('已报到', '已报到'), ('', '')]),
        ),
    ]
