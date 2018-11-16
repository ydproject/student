# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0008_payment_plan_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_item',
            name='action',
            field=models.CharField(verbose_name='费用期间', max_length=500, default='All'),
        ),
    ]
