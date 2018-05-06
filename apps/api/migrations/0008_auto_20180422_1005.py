# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-22 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180417_2043'),
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
        migrations.AddField(
            model_name='result',
            name='desp',
            field=models.TextField(default='', verbose_name='\u6267\u884c\u60c5\u51b5'),
        ),
    ]