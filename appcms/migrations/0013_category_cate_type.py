# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0012_auto_20150518_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cate_type',
            field=models.CharField(default='NORMAL', max_length=5, choices=[('SIGLE', '单页面分类'), ('NORMAL', '常规分类')]),
        ),
    ]
