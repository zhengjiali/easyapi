# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180507_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='cookies',
            new_name='response_cookies',
        ),
        migrations.RenameField(
            model_name='result',
            old_name='headers',
            new_name='response_headers',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='deleted',
            new_name='is_deleted',
        ),
        migrations.AddField(
            model_name='case',
            name='encryption_type',
            field=models.IntegerField(default=0, verbose_name='\u52a0\u5bc6\u65b9\u5f0f'),
        ),
        migrations.AddField(
            model_name='result',
            name='desp',
            field=models.TextField(default='', verbose_name='\u6267\u884c\u60c5\u51b5'),
        ),
    ]