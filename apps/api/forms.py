# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/2/12 上午11:03'


from django import forms

class ApiForm(forms.Form):
    path = forms.CharField(required=True)
    method = forms.CharField(required=True)
    headers = forms.CharField(required=False)
    parameter = forms.CharField(required=False)
    name = forms.CharField(required=True)
    tag = forms.CharField(required=True)
    description = forms.CharField(required=False)
