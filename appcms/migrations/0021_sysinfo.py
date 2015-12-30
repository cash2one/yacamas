# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0020_category_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=60, default='')),
                ('value', models.CharField(max_length=5000, default='')),
            ],
        ),
    ]
