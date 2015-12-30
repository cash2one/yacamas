# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0006_auto_20150508_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='position_id',
            field=models.CharField(max_length=60, blank=True, default='0'),
        ),
    ]
