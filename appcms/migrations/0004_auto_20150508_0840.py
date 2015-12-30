# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0003_auto_20150508_0838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archive',
            old_name='last_edit_time',
            new_name='edit_time',
        ),
    ]
