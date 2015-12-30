# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0008_auto_20150508_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='author',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='archive',
            name='description',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='keywords',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='referer',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='title',
            field=models.CharField(default='', max_length=60),
        ),
    ]
