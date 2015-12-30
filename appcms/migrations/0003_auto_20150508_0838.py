# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0002_auto_20150508_0707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archive',
            old_name='keyword',
            new_name='keywords',
        ),
    ]
