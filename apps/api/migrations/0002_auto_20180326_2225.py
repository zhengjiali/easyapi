# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-26 14:25
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=100, verbose_name='api\u8def\u5f84')),
                ('method', models.CharField(choices=[('get', 'get'), ('post', 'post'), ('put', 'put')], max_length=10)),
                ('name', models.CharField(max_length=20, verbose_name='api\u540d\u79f0')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='api\u63cf\u8ff0')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('is_deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'verbose_name': 'API',
                'verbose_name_plural': 'API',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u7528\u4f8b\u540d\u79f0')),
                ('headers', models.CharField(blank=True, max_length=600, null=True)),
                ('cookies', models.CharField(blank=True, max_length=600, null=True)),
                ('parameter', models.CharField(blank=True, max_length=200, null=True)),
                ('validation', models.CharField(blank=True, max_length=200, null=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('is_deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Api', verbose_name='\u6240\u5c5eapi')),
            ],
            options={
                'verbose_name': 'Api\u914d\u7f6e',
                'verbose_name_plural': 'Api\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='Proj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('father_id', models.IntegerField(default=0, verbose_name='\u4e0a\u4e00\u7ea7\u9879\u76eeid')),
                ('deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u540d',
                'verbose_name_plural': '\u9879\u76ee\u540d',
            },
        ),
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField(verbose_name='\u54cd\u5e94\u72b6\u6001\u7801')),
                ('response', models.TextField(verbose_name='\u54cd\u5e94\u7ed3\u679c')),
                ('is_pass', models.IntegerField(default=0, verbose_name='0\uff1a\u9ed8\u8ba4\u4e0d\u586b\u5199\uff0c1\uff1a\u901a\u8fc7\uff0c-1\uff1a\u4e0d\u901a\u8fc7')),
                ('task_id', models.IntegerField(default=0, verbose_name='0\uff1a\u6d4b\u8bd5\uff0c\u5176\u4ed6\uff1a\u4efb\u52a1id')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Case', verbose_name='\u6d4b\u8bd5\u7528\u4f8b')),
            ],
            options={
                'verbose_name': '\u6d4b\u8bd5\u7ed3\u679c',
                'verbose_name_plural': '\u6d4b\u8bd5\u7ed3\u679c',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u6807\u7b7e\u540d\u79f0')),
                ('deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7279\u6027',
                'verbose_name_plural': '\u7279\u6027',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tag', verbose_name='\u7528\u4f8b\u6807\u7b7e'),
        ),
        migrations.AddField(
            model_name='case',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='api',
            name='proj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Proj', verbose_name='\u6240\u5c5e\u9879\u76ee'),
        ),
        migrations.AddField(
            model_name='api',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba'),
        ),
    ]