# -*- coding:utf-8 -*-
import json
import requests

# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from .forms import ApiForm
from .models import  *

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
                if ApiConfig.objects.get(path=api_path) or ApiConfig.objects.get(name=api_name):
                    return render(request,"test.html",{"msg":u"该api已存在","api_form":api_form})
            except Exception:
                pass

            api_method = request.POST.get("method","")
            api_parameter = request.POST.get("parameter","")
            api_description = request.POST.get("description","")
            api_headers = request.POST.get("headers","")
            tag = request.POST.get("tag","")
            api = ApiConfig()
            api.description = api_description
            api.path = api_path
            api.headers = api_headers
            api.parameter = api_parameter
            api.method = api_method
            api.name = api_name
            api.user = User.objects.get(username='zhengjiali')
            api.tag = Tag.objects.get(name=tag)
            api.save()
            if ApiConfig.objects.get(path=api_path):
                return render(request,"save_sucess.html")
            else:
                return render(request,"test.html",{"msg":u"保存失败！","api_form":api_form})
        else:
            return render(request,"test.html",{"api_form":api_form})


class TestView(View):
    def get(self,request,api_id):
        api = ApiConfig.objects.get(id=api_id)
        return render(request,"test2.html",{"api":api})

    def post(self,request):
        apiId = request.POST.get("apiId","")
        api = ApiConfig.objects.get(id=apiId)
        url = api.path
        if not api.parameter:
            para = ''
        else:
            para = json.loads(api.parameter)
        if not api.headers:
            headers = ''
        else:
            headers = json.loads(api.headers)
        method = api.method
        if method == 'post':
            r=requests.post(url,data=para,headers=headers)
        elif method == 'get':
            r=requests.get(url,data=para,headers=headers)

        if r.status_code == 200:
            return JsonResponse({"status" : 0,"message" : u"测试成功","result" : r.text.decode("unicode-escape") })
        else:
            return JsonResponse({"status" : 1,"message" : u"测试失败"})

