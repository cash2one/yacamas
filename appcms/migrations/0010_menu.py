# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0009_auto_20150509_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(default='', max_length=60)),
                ('url', models.CharField(default='', max_length=260)),
                ('m_type', models.CharField(default='back', max_length=10)),
                ('code', models.CharField(default='', max_length=30)),
                ('perm_id', models.PositiveSmallIntegerField(default=0)),
                ('status', models.PositiveSmallIntegerField(default=99)),
                ('pid', models.PositiveSmallIntegerField()),
                ('path', models.CharField(max_length=60)),
                ('has_child', models.BooleanField()),
                ('depth', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
