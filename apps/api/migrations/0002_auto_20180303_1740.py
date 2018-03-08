# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-03 09:40
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
            name='ApiConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='case\u540d\u79f0')),
                ('headers', models.CharField(blank=True, max_length=600, null=True)),
                ('cookies', models.CharField(blank=True, max_length=600, null=True)),
                ('parameter', models.CharField(blank=True, max_length=200, null=True)),
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
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u7279\u6027\u540d\u79f0')),
                ('deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7279\u6027',
                'verbose_name_plural': '\u7279\u6027',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u6807\u7b7e\u540d')),
                ('father_id', models.IntegerField(default=0, verbose_name='\u4e0a\u4e00\u7ea7\u6807\u7b7eid')),
                ('deleted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=200, verbose_name='\u9a8c\u8bc1\u5173\u952e\u5b57')),
                ('value', models.CharField(max_length=200, verbose_name='\u9a8c\u8bc1\u503c')),
                ('api_id', models.IntegerField(verbose_name='\u9a8c\u8bc1\u63a5\u53e3id')),
            ],
            options={
                'verbose_name': 'API\u6821\u9a8c',
                'verbose_name_plural': 'API\u6821\u9a8c',
            },
        ),
        migrations.AddField(
            model_name='apiconf',
            name='character',
            field=models.ManyToManyField(to='api.Character'),
        ),
        migrations.AddField(
            model_name='apiconf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='api',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tag', verbose_name='api\u6240\u5c5e\u6807\u7b7e'),
        ),
        migrations.AddField(
            model_name='api',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba'),
        ),
    ]
