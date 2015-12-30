# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabb',
            name='id_forever',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tabb',
            name='ref_cnt',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
