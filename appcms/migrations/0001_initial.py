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
                ('keyword', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('referer', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField()),
                ('last_edit_time', models.DateTimeField(auto_now=True)),
                ('position_id', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField()),
            ],
            options={
                'permissions': (('add_arch', '添加文章'), ('edit_arch', '编辑文章'), ('get_arch', '读取文章'), ('del_arch', '删除文章')),
            },
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
            options={
                'permissions': (('add_cate', '添加分类'), ('edit_cate', '编辑分类'), ('get_cate', '读取（查看）分类'), ('del_cate', '删除分类')),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'permissions': (('add_pos', '添加分类'), ('edit_pos', '编辑分类'), ('get_pos', '读取分类'), ('del_pos', '删除分类')),
            },
        ),
    ]
