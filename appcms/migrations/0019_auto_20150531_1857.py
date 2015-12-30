# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0018_menu_list_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alias',
            field=models.CharField(max_length=60),
        ),
    ]
