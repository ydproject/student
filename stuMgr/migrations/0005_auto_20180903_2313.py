# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0004_auto_20180902_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('term_name', models.CharField(verbose_name='名称', max_length=20)),
            ],
            options={
                'verbose_name': '学期',
                'verbose_name_plural': '学期',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='paymentinfo',
            name='termId',
            field=models.ForeignKey(verbose_name='学期', to='stuMgr.TermInfo'),
        ),
    ]
