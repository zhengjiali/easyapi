# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-12 05:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180212_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiconfig',
            name='tag',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='api.Tag', verbose_name='api\u6240\u5c5e\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='apiconfig',
            name='user',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba'),
        ),
    ]
