# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuMgr', '0007_auto_20181016_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_plan',
            name='flag',
            field=models.BooleanField(verbose_name='是否激活', default=False),
        ),
    ]
