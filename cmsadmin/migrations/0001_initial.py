# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('cate_id', models.IntegerField()),
                ('title', models.CharField(max_length=60)),
                ('author_id', models.PositiveSmallIntegerField()),
                ('summary', models.TextField()),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('last_edit_time', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField()),
                ('position_id', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('pid', models.PositiveSmallIntegerField()),
                ('path', models.CharField(max_length=60)),
                ('has_child', models.BooleanField()),
                ('depth', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
    ]
