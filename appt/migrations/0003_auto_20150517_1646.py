# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appt', '0002_auto_20150517_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taba',
            name='tb',
        ),
        migrations.AddField(
            model_name='taba',
            name='tb',
            field=models.ManyToManyField(to='appt.TabB'),
        ),
        migrations.RemoveField(
            model_name='taba',
            name='tc',
        ),
        migrations.AddField(
            model_name='taba',
            name='tc',
            field=models.ManyToManyField(to='appt.TabC'),
        ),
    ]
