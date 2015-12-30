# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0015_auto_20150518_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='tpl',
            field=models.CharField(max_length=50, default=''),
        ),
    ]
