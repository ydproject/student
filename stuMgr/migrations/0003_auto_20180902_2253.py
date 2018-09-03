# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0002_payment_item_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_item',
            name='item_name',
            field=models.CharField(verbose_name='名称', max_length=20),
        ),
    ]
