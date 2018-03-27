# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/3/27 下午4:09'
import json
import requests
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse,HttpResponse
from .forms import *
from .models import  Api,Tag,Case,Proj

def dealParam(parameter):
    if parameter:
        plist = parameter.split('&')
        data = {}
        for p in plist:
            l = p.split('=')
            data[l[0]] = l[1]
        return data

class CaseTestView(View):
    def get(self,request,case_id):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        if not Case.objects.get(id=int(case_id)):
            return render(request,"error.html")
        case = Case.objects.get(id=int(case_id))
        return render(request,"CaseTest.html",{"case":case})

    def post(self,request,case_id):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        if not Case.objects.get(id=int(case_id)):
            return JsonResponse({"msg":u"不存在"})
        case = Case.objects.get(id=int(case_id))
        api = case.api
        url = api.path
        parameter = case.parameter
        headers = case.headers
        cookies = case.cookies
        if headers:
            headers = json.loads(headers)
        if cookies:
            cookies = json.loads(cookies)
        method = api.method
        if method == 'post':
            if parameter:
                parameter = dealParam(parameter)
            r=requests.post(url,data=parameter,headers=headers,cookies=cookies)
        elif method == 'get':
            r=requests.get(url+'?'+parameter,headers=headers,cookies=cookies)

        if r.status_code == 200:
            return JsonResponse({"status" : 0,"message" : u"测试成功","result" : {"text":r.text.decode("unicode-escape"),"c":r.cookies.__str__(),"h":r.headers.__str__()}})
        else:
            return JsonResponse({"status" : 1,"message" : u"测试失败"})
