# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcms', '0013_category_cate_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cate_type',
            field=models.CharField(choices=[('SIGLE', '单页面分类'), ('NORMAL', '常规分类')], default='NORMAL', max_length=6),
        ),
    ]
