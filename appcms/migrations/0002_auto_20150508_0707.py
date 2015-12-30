# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='author_id',
        ),
        migrations.AddField(
            model_name='archive',
            name='author',
            field=models.CharField(max_length=30, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='archive',
            name='description',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='keyword',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='position_id',
            field=models.CharField(max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='referer',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='archive',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
