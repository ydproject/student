# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_item',
            name='item_name',
            field=models.CharField(verbose_name='种类名称', max_length=20, default='学费all'),
            preserve_default=False,
        ),
    ]
