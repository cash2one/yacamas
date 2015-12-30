# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0010_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='alias',
            field=models.CharField(max_length=60, unique=True, default=''),
            preserve_default=False,
        ),
    ]
