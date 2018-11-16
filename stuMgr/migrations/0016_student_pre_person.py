# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0015_auto_20181115_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='pre_person',
            field=models.CharField(verbose_name='预收费责任人', max_length=50, default=''),
        ),
    ]
