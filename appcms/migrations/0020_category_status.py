# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0019_auto_20150531_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.PositiveSmallIntegerField(default=99),
        ),
    ]
