# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0013_flowing_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowing',
            name='type',
            field=models.CharField(verbose_name='收付款', max_length=20, default='收款', choices=[('收款', '收款'), ('退款', '退款')]),
        ),
    ]
