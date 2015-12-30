# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0014_auto_20150518_0941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={},
        ),
        migrations.AlterField(
            model_name='category',
            name='cate_type',
            field=models.CharField(default='NORMAL', max_length=6, choices=[('SINGLE', '单页面分类'), ('NORMAL', '常规分类')]),
        ),
    ]
