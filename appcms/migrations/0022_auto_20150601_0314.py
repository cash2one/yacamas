# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0021_sysinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysinfo',
            name='key',
            field=models.CharField(max_length=60, default='', unique=True),
        ),
    ]
