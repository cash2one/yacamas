# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TabA',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TabB',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('path', models.CharField(max_length=239)),
                ('file_name', models.CharField(max_length=60)),
                ('ref_cnt', models.PositiveSmallIntegerField()),
                ('id_forever', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TabC',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('utitle', models.CharField(max_length=60)),
                ('ucontent', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='taba',
            name='tb',
            field=models.ForeignKey(to='appt.TabB'),
        ),
        migrations.AddField(
            model_name='taba',
            name='tc',
            field=models.ForeignKey(to='appt.TabC'),
        ),
    ]
