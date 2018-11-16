# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0010_auto_20181018_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinfo',
            name='action',
            field=models.CharField(verbose_name='费用期间', max_length=20, default='All', choices=[('All', 'All'), ('1月', '1月'), ('2月', '2月'), ('3月', '3月'), ('4月', '4月'), ('5月', '5月'), ('6月', '6月'), ('7月', '7月'), ('8月', '8月'), ('9月', '9月'), ('10月', '10月'), ('11月', '11月'), ('12月', '12月')]),
        ),
    ]
