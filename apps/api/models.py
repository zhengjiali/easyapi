# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"标签名")
    father_id = models.IntegerField(default=0,verbose_name=u"上一级标签id")
    create_time = models.DateTimeField(default=datetime.now,verbose_name=u"创建时间")

    class Meta:
        verbose_name = u"标签"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class ApiConfig(models.Model):
    path = models.CharField(max_length=100,verbose_name=u"api路径")
    method = models.CharField(max_length=10,choices=(("get","get"),("post","post"),("put","put")))
    headers = models.CharField(max_length=10000,null=True,blank=True)
    parameter = models.CharField(max_length=10000,null=True,blank=True)
    name = models.CharField(max_length=20,verbose_name=u"api名称")
    description = models.CharField(max_length=200,verbose_name=u"api描述",null=True,blank=True)
    tag = models.ForeignKey(Tag,verbose_name=u"api所属标签")
    user = models.ForeignKey(User,verbose_name=u"创建人")
    create_time = models.DateTimeField(default=datetime.now,verbose_name=u"创建时间")
    update_time = models.DateTimeField(default=datetime.now,verbose_name=u"修改时间")
    is_deleted = models.IntegerField(default=0,verbose_name=u"是否删除")

    class Meta:
        verbose_name = u"API配置"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Validation(models.Model):
    key = models.CharField(max_length=200,verbose_name=u"验证关键字")
    value = models.CharField(max_length=200,verbose_name=u"验证值")
    api_id = models.IntegerField(verbose_name=u"验证接口id")

    class Meta:
        verbose_name = u"API校验"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


