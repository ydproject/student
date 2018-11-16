# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0009_auto_20181016_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinfo',
            name='status',
            field=models.CharField(verbose_name='缴费情况', max_length=20, default='未缴费', choices=[('已缴费', '已缴费'), ('未缴费', '未缴费')]),
        ),
    ]
