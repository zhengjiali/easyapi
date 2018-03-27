# -*- coding:utf-8 -*-
import json
import requests
from django.core import serializers

# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse,HttpResponse
from .forms import *
from .models import  Api,Tag,Case,Proj

# Create your views here.

def saveParam(parameter):
    '''
    将para1=data1&para2=data2转成{"para1":"data1","para2":"data2"}
    :param parameter:
    :return: string
    '''
    if parameter:
        plist = parameter.split('&')
        data = {}
        for p in plist:
            l = p.split('=')
            data[l[0]] = l[1]
        return data

class ApiView(View):
    def get(self,request,api_id):
        api = Api.objects.get(id=int(api_id))
        cases = api.get_all_case()
        allcase = list(api.get_all_case().values("id","name","headers","cookies","parameter"))
        data = {"status":0,"api":{"path":api.path,"method":api.method,"name":api.name,"description":api.description}}
        data["cases"]=allcase
        return JsonResponse(data)

class ApiNewView(View):
    def get(self,request):
        if request.user.is_authenticated():
            user = request.user
            projs = Proj.objects.all()
            return render(request,"new_api.html",{"user":user,"projs":projs})
        else:
            return render(request,"login.html")

    def post(self,request):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        api_form = ApiForm(request.POST)
        if api_form.is_valid():
            api_path = request.POST.get("path","")
            api_name = request.POST.get("name","")
            proj_id = request.POST.get("project","")
            project = Proj.objects.get(id=int(proj_id))

            try:
                if Api.objects.get(path=api_path,proj=project):
                    return JsonResponse({"msg":u"该api已存在","status":1})
            except Exception:
                pass

            api_method = request.POST.get("method","")
            api_description = request.POST.get("description","")
            api = Api()
            api.description = api_description
            api.path = api_path
            api.method = api_method
            api.name = api_name
            api.proj = project
            api.user = request.user
            api.save()
            if Api.objects.get(path=api_path):
                return JsonResponse({"msg":u"新建成功","status":0})
            else:
                return JsonResponse({"msg":u"新建失败","status":-1})
        else:
            return JsonResponse({"msg":u"验证失败","status":1})

class ApiQueryView(View):

    def get(self,request):
        api_all = Api.objects.all()
        sortType = request.GET.get("sortType","desc")
        pj = request.GET.get("project",0)
        kw = request.GET.get("kw","")
        if pj!= 0:
            proj = Proj.objects.get(id=int(pj))
            apis = api_all.filter(proj=proj,is_deleted=0)
        else:
            apis = api_all.filter(is_deleted=0)
        if sortType == 'desc':
            apis = apis.order_by("-update_time")
        elif sortType == 'asc':
            apis = apis.order_by("update_time")
        if kw:
            apis = apis.filter(name__contains=kw)
        data = serializers.serialize('json', apis,use_natural_foreign_keys=True)
        return HttpResponse(data)

def data_list(request):
    apiId = request.GET.get("apiId", "")
    api = Api.objects.get(id=apiId)
    result = {"status":0,"message":u"获取api列表成功"}
    result["data"]=dict(list=list(Case.objects.filter(api=api).values('id','name','parameter')))
    return JsonResponse(result)


class CaseNewView(View):
    def get(self,request,api_id):
        api = Api.objects.get(id=int(api_id))
        return render(request,"data_list.html",{"api":api})

    def post(self,request,api_id):
        if not request.user.is_authenticated():
            return render(request,"login.html")
        case_form = CaseForm(request.POST)
        if case_form.is_valid():
            if not Api.objects.filter(id=int(api_id),is_deleted=0):
                return JsonResponse({"msg":u"该api不存在","status":-1})
            case_name = request.POST.get("name","")
            case_headers = request.POST.get("headers","")
            case_cookies = request.POST.get("cookies","")
            case_api = Api.objects.get(id=int(api_id))
            case_validation = request.POST.get("validation","")
            case_parameter = request.POST.get("parameter","")
            case_tag_id = request.POST.get("tag",0)

            try:
                if Case.objects.get(name=case_name,api=case_api):
                    return JsonResponse({"msg":u"该用例已存在","status":-1})
            except Exception:
                pass

            case = Case()
            case.name = case_name
            case.user = request.user
            case.api = case_api
            case.headers = case_headers
            case.cookies = case_cookies
            case.validation = case_validation
            case.parameter = case_parameter
            if case_tag_id!=0:
                case_tag=Tag.objects.get(id=int(case_tag_id))
                case.tag = case_tag
            case.save()
            return JsonResponse({"msg":u"新建用例成功","status":0})
        else:
            return JsonResponse({"msg":u"校验失败","status":-1})





def get_tags(request):
    return JsonResponse(dict(data=list(Tag.objects.filter(deleted=0).values('id','name','father_id','create_time'))))
