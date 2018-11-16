# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0006_auto_20181011_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowing',
            name='person',
            field=models.CharField(verbose_name='责任人', max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='person',
            field=models.CharField(verbose_name='责任人', max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='prement',
            name='person',
            field=models.CharField(verbose_name='责任人', max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='person',
            field=models.CharField(verbose_name='责任人', max_length=50, default=''),
        ),
    ]
