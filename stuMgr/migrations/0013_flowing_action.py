# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0012_auto_20181022_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowing',
            name='action',
            field=models.CharField(verbose_name='方式', max_length=20, default='现金', choices=[('微信', '微信'), ('支付宝', '支付宝'), ('现金', '现金'), ('银行卡', '银行卡')]),
        ),
    ]
