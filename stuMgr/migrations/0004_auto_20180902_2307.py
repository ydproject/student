# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0003_auto_20180902_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowing',
            name='action',
        ),
        migrations.RemoveField(
            model_name='flowing',
            name='time',
        ),
        migrations.AlterField(
            model_name='flowing',
            name='flowing',
            field=models.FloatField(verbose_name='金额', default=0.0),
        ),
        migrations.AlterField(
            model_name='paymentinfo',
            name='money',
            field=models.FloatField(verbose_name='金额', default=0.0),
        ),
        migrations.AlterField(
            model_name='prement',
            name='premoney',
            field=models.FloatField(verbose_name='预收费', default=0.0),
        ),
    ]
