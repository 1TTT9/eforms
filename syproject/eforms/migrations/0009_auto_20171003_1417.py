# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-10-03 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eforms', '0008_auto_20171003_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='efmrequest03',
            name='department',
            field=models.TextField(max_length=50, verbose_name='\u90e8\u9580'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='project_code',
            field=models.TextField(max_length=50, verbose_name='\u5de5\u4ee3'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='receiver_account',
            field=models.TextField(max_length=50, verbose_name='\u5e33\u865f'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='receiver_bank',
            field=models.TextField(max_length=100, verbose_name='\u958b\u6236\u884c\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='receiver_name',
            field=models.TextField(max_length=50, verbose_name='\u59d3\u540d/\u516c\u53f8\u540d\u7a31'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='title',
            field=models.TextField(max_length=30, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='efmrequest03',
            name='unknown_02',
            field=models.DateTimeField(max_length=50, verbose_name='\u5831\u92b7\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='efmrequest06',
            name='department',
            field=models.TextField(max_length=50, verbose_name='\u90e8\u9580'),
        ),
        migrations.AlterField(
            model_name='efmrequest06',
            name='project_code',
            field=models.TextField(max_length=50, verbose_name='\u5de5\u4ee3'),
        ),
        migrations.AlterField(
            model_name='efmrequest06',
            name='title',
            field=models.TextField(max_length=30, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='ereview',
            name='title',
            field=models.TextField(max_length=30, verbose_name='\u6807\u9898'),
        ),
    ]
