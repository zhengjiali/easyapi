# -*- coding:utf-8 -*-
import json
import requests

# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from .forms import ApiForm
from .models import  Api,Tag,Validation,ApiConf,Character

# Create your views here.

class ApiView(View):

    def get(self,request):
        if request.user.is_authenticated():
            user = request.user
            return render(request,"test.html",{"user":user})
        else:
            return render(request,"login.html")

    def post(self,request):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        api_form = ApiForm(request.POST)
        if api_form.is_valid():
            api_path = request.POST.get("path","")
            api_name = request.POST.get("name","")
            try:
                if Api.objects.get(path=api_path) or Api.objects.get(name=api_name):
                    return render(request,"test.html",{"msg":u"该api已存在","api_form":api_form})
            except Exception:
                pass

            api_method = request.POST.get("method","")
            # api_parameter = request.POST.get("parameter","")
            api_description = request.POST.get("description","")
            # api_headers = request.POST.get("headers","")
            tag = request.POST.get("tag","")
            api = Api()
            api.description = api_description
            api.path = api_path
            # api.headers = api_headers
            # api.parameter = api_parameter
            api.method = api_method
            api.name = api_name
            api.user = request.user
            api.tag = Tag.objects.get(name=tag)
            api.save()
            if Api.objects.get(path=api_path):
                return render(request,"save_sucess.html")
            else:
                return render(request,"test.html",{"msg":u"保存失败！","api_form":api_form})
        else:
            return render(request,"test.html",{"api_form":api_form})


class TestView(View):
    def get(self,request,api_id):
        api = Api.objects.get(id=api_id)
        return render(request,"test2.html",{"api":api})

    def post(self,request):
        apiId = request.POST.get("apiId","")
        api = Api.objects.get(id=apiId)
        url = api.path
        parameter = request.POST.get("parameter","")
        headers = request.POST.get("headers","")
        cookies = request.POST.get("cookies","")
        if parameter:
            parameter = json.loads(parameter)
        if headers:
            headers = json.loads(headers)
        if cookies:
            cookies = json.loads(cookies)
        method = api.method
        if method == 'post':
            r=requests.post(url,data=parameter,headers=headers,cookies=cookies)
        elif method == 'get':
            r=requests.get(url,data=parameter,headers=headers,cookies=cookies)

        if r.status_code == 200:
            return JsonResponse({"status" : 0,"message" : u"测试成功","result" : {"text":r.text.decode("unicode-escape"),"c":r.cookies.__str__(),"h":r.headers.__str__()}})
        else:
            return JsonResponse({"status" : 1,"message" : u"测试失败"})


class ApiListView(View):

    def get(self,request):
        return render(request,"data_list.html")


def data_list(request):
    apiId = request.GET.get("apiId", "")
    api = Api.objects.get(id=apiId)
    result = {"status":0,"message":u"获取api列表成功"}
    result["data"]=dict(list=list(ApiConf.objects.filter(api=api).values('id','name','parameter')))
    return JsonResponse(result)


def apis_list(request):
    return JsonResponse(dict(data=list(Api.objects.values('id','name','method','path'))))

def saveconf(request):
    if not request.user.is_authenticated():
        return render(request,"login.html")

    apiId = request.POST.get("apiId","")
    api_conf = ApiConf()
    api_conf.api = Api.objects.get(id=apiId)
    api_conf.headers = request.POST.get("headers","")
    api_conf.cookies = request.POST.get("cookies","")
    api_conf.parameter = request.POST.get("parameter","")
    api_conf.user = request.user
    api_conf.save()

    return JsonResponse({"status":0,"message":u"保存成功！"})

class ApiConfListView(View):
    def get(self,request,api_id):
        api = Api.objects.get(id=api_id)
        return render(request,"data_list.html",{"api":api})

def get_tags(request):
    return JsonResponse(dict(data=list(Tag.objects.filter(deleted=0).values('id','name','father_id','create_time'))))
