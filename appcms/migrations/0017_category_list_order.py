# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0016_archive_tpl'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='list_order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
