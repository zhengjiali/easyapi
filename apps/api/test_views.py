# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/3/27 下午4:09'
import json
import requests
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse,HttpResponse
from .forms import *
from task.models import runtime_env
from .models import  Api,Tag,Case,Proj,Result

def dealParam(parameter):
    if parameter:
        para = json.loads(parameter)
        data = '&'.join( [ item+'='+str(para[item]) for item in para.iterkeys() ] )
        return data

def save_result(r,case,task_id):
    result = Result()
    result.case = case
    result.request_headers = r.headers.__str__()
    result.response_cookies = r.cookies.__str__()
    result.response = r.text.decode("unicode-escape")
    result.status_code = r.status_code
    result.request_headers = r.request.headers.__str__()
    result.url = r.url
    result.task_id = task_id
    result.save()

def save_exception(e,case,task_id):
    result = Result()
    result.case = case
    result.status_code = 0
    result.task_id = task_id
    result.desp = e.message
    result.save()

def test_case(env_id,case):
    parameter = case.parameter
    headers = case.headers
    cookies = case.cookies
    if headers:
        headers = json.loads(headers)
    if cookies:
        cookies = json.loads(cookies)
    api = case.api
    env = runtime_env.objects.get(id=env_id)
    url = env.uri+api.path
    method = api.method
    if method == 'post':
        if parameter:
            parameter = json.loads(parameter)
        r = requests.post(url, data=parameter, headers=headers, cookies=cookies)
    elif method == 'get':
        if parameter:
            parameter = dealParam(parameter)
            r = requests.get(url + '?' + parameter, headers=headers, cookies=cookies)
        else:
            r = requests.get(url,headers=headers,cookies=cookies)

    return r


class CaseTestView(View):
    def get(self,request,case_id):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        if not Case.objects.get(id=int(case_id)):
            return render(request,"error.html")
        case = Case.objects.get(id=int(case_id))
        return render(request,"CaseTest.html",{"case":case})

    def post(self,request,case_id):
        if not Case.objects.get(id=int(case_id)):
            return JsonResponse({"msg":u"不存在"})
        task_id = request.POST.get("task_id",'')
        if task_id:
            task_id = int(task_id)
        else:
            task_id = 0
        case = Case.objects.get(id=int(case_id))
        r = test_case(1,case)

        save_result(r,case,task_id)

        if r.status_code == 200:
            return JsonResponse({"status" : 0,"message" : u"测试成功","result" : {"status_code":r.status_code,"url":r.url,"text":r.json(),"c":r.cookies.__str__(),"h":r.headers.__str__()}})
        else:
            return JsonResponse({"status" : 1,"message" : u"测试失败"})
