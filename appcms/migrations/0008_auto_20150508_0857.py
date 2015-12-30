# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0007_auto_20150508_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='status',
            field=models.PositiveSmallIntegerField(default=99),
        ),
    ]
