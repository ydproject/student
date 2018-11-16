# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0014_flowing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='premoney',
            field=models.FloatField(verbose_name='预收费', default=0.0),
        ),
        migrations.AlterField(
            model_name='flowing',
            name='remark',
            field=models.TextField(verbose_name='备注', max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='prement',
            name='person',
            field=models.CharField(verbose_name='责任人', max_length=20, default=''),
        ),
        migrations.AlterField(
            model_name='prement',
            name='remark',
            field=models.TextField(verbose_name='备注', max_length=20, default=''),
        ),
    ]
