# -*- coding:utf-8 -*-
import json
import time
import os

from users.views import login_required,LoginRequiredView
from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse,HttpResponse
from .forms import *
from .models import  Api,Tag,Case,Proj,runtime_env
from django.contrib.auth.models import User
from task.models import plan
from . import dealCase

# Create your views here.

PER_PAGE_COUNT=10

@login_required
def api_list(request):
    '''
    api列表渲染页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        projs = Proj.objects.filter(deleted=0)
        apis = Api.objects.filter(is_deleted=0).order_by('-update_time')
        return render(request,'api_list.html',{"projs":projs,"apis":apis}) #todo

@login_required
def edit_api(request,api_id):
    '''
    api编辑渲染页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        api = Api.objects.get(id=int(api_id))
        projs = Proj.objects.filter(deleted=0).order_by("id")
        return render(request,'api_edit.html',{"api":api,'projs':projs})


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

def get_projects(request):
    if request.method == 'GET':
        proj = Proj.objects.filter(father_id=0,deleted=0)
        sum = proj.count()
        return JsonResponse(dict(count=sum,projs=list(proj.values('id', 'name'))))

    else:
        return JsonResponse({})

def get_slice(count,page):
    '''
    根据页码，返回QuerySet对应页码的切片区间
    :param count: 需要分页的总数目
    :param page: 页码
    :return: lowpos,highpos
    '''
    max = count/PER_PAGE_COUNT+1 if count%PER_PAGE_COUNT else count/PER_PAGE_COUNT
    lowpos = PER_PAGE_COUNT*(page-1)
    if page>0 and page<max:
        highpos = lowpos+10
    elif page == max:
        highpos=count
    else:
        lowpos = highpos = count

    return (lowpos,highpos)

class ApiView(View):
    def get(self,request,api_id):
        api = Api.objects.get(id=int(api_id))
        cases = api.get_all_case()
        allcase = list(api.get_all_case().values("id","name","headers","cookies","parameter"))
        data = {"status":0,"api":{"path":api.path,"method":api.method,"name":api.name,"description":api.description}}
        data["cases"]=allcase
        return JsonResponse(data)

class ApiNewView(LoginRequiredView,View):
    def get(self,request):
        projs = Proj.objects.all()
        return render(request,"api_add.html",{"user":request.user,"projs":projs})

    def post(self,request):
        '''
        新建／保存api
        :param request:
        :return:
        '''
        api_form = ApiForm(request.POST)
        if api_form.is_valid():
            api_path = request.POST.get("path","")
            api_name = request.POST.get("name","")
            proj_id = request.POST.get("project","")
            project = Proj.objects.get(id=int(proj_id))
            api_method = request.POST.get("method", "")
            api_description = request.POST.get("description", "")
            api_id = int(request.POST.get("api_id",-1))

            if api_id != -1:
                if Api.objects.filter(path=api_path,is_deleted=0,proj=project).exclude(id=api_id) or Api.objects.filter(name=api_name,is_deleted=0,proj=project).exclude(id=api_id):
                    return JsonResponse({"msg":u"该api已存在","status":1})
                api = Api.objects.filter(id=int(request.POST.get("api_id")),is_deleted=0)[0]
                if not api:
                    return JsonResponse({"msg":u"该api不存在","status":2})
            elif Api.objects.filter(path=api_path,proj=project,is_deleted=0) or Api.objects.filter(name=api_name,proj=project,is_deleted=0):
                    return JsonResponse({"msg":u"该api已存在","status":1})
            else:
                api = Api()

            api.description = api_description
            api.path = api_path
            api.method = api_method.lower()
            api.name = api_name
            api.proj = project
            api.user = request.user
            # api.user = User.objects.get(id=1) #todo 注释
            try:
                api.save()
                return JsonResponse({"msg":u"保存成功","status":0})
            except Exception as e:
                return JsonResponse({"msg":u"保存失败","status":-1})
        else:
            return JsonResponse({"msg":u"验证失败","status":3})

class ApiQueryView(View):
    def get(self,request):
        api_all = Api.objects.filter(is_deleted=0)
        count = api_all.count()
        sortType = request.GET.get("sortType","desc")
        pj = request.GET.get("project","")
        kw = request.GET.get("kw","")
        page = request.GET.get('currPage',1)
        if pj!= "":
            proj = Proj.objects.get(id=int(pj))
            apis = api_all.filter(proj=proj)
        else:
            apis = api_all
        if sortType == 'desc':
            apis = apis.order_by("-update_time")
        elif sortType == 'asc':
            apis = apis.order_by("update_time")
        if kw:
            apis = apis.filter(name__contains=kw)
        sum = apis.count()
        low,high = get_slice(count,int(page))
        apis = apis[low:high]
        data1 = [ i.get_values('id','name','path','method','description','proj','user','update_time') for i in apis]
        return JsonResponse({"count":sum,"currentPage":page,"data":data1})


def data_list(request):
    apiId = request.GET.get("apiId", "")
    api = Api.objects.get(id=apiId)
    result = {"status":0,"message":u"获取api列表成功"}
    result["data"]=dict(list=list(Case.objects.filter(api=api).values('id','name','parameter')))
    return JsonResponse(result)

class InitCaseView(LoginRequiredView,View):
    def get(self,request,api_id):
        tags = Tag.objects.filter(is_deleted=0)
        api = Api.objects.filter(id=int(api_id),is_deleted=0)
        if api:
            apis = api[0].get_values("id","name","path","method","proj","description")
            return render(request,'api_initcase.html',{"api":apis,"tags":tags})
        else:
            return render(request,'wrong.html')

class CaseNewView(LoginRequiredView,View): #todo 增加权限LoginRequiredView
    def get(self,request,api_id):
        tags = Tag.objects.filter(is_deleted=0)
        api = Api.objects.filter(id=int(api_id),is_deleted=0)
        if api:
            apis = api[0].get_values("id", "name", "path", "method", "proj","description")
            #此处获取tag_id# 并渲染至界面，界面先默认传1/2，用例类型数据默认为： api接口：101，其他102
            return render(request,'api_testcase_add.html',{"api":apis,"tags":tags})
        else:
            return render(request,'wrong.html')

    def post(self,request):
        data = json.loads(request.body)
        case_form = False
        if data["profile"]["case_name"] and data["api_id"]!=0:
            case_form = True
        if case_form:
            case_name = str(data["profile"]["case_name"])
            api_id = data["api_id"]
            if not Api.objects.filter(id=int(api_id),is_deleted=0):
                return JsonResponse({"msg":u"该api不存在","status":1})
            case_headers = json.dumps(data["headers"],encoding='UTF-8',ensure_ascii=False)
            case_cookies = json.dumps(data["cookies"],encoding='UTF-8',ensure_ascii=False)
            case_api = Api.objects.get(id=int(api_id))
            case_validation = data["validations"]
            parameter = json.dumps(data["parameters"],encoding='UTF-8',ensure_ascii=False)
            if parameter != '{}':
                case_parameter = parameter
            else:
                case_parameter = data["plainText"]
 
            case_tag_id = int(data["profile"]["case_type"])
            if data["profile"].has_key("case_enctype"):
                case_encryption_type = int(data["profile"]["case_enctype"])
            else:
                case_encryption_type = 0
            if data.has_key("case_id"):
                case_id = int(data["case_id"])
            else:
                case_id = 0
            if  case_id != 0: #修改已存在的case
                if Case.objects.filter(name=case_name,api=case_api,is_deleted=0).exclude(id=case_id):
                    return JsonResponse({"msg":u"该用例已存在","status":2})
                case = Case.objects.filter(id=case_id,is_deleted=0)[0]
                if not case:
                    return JsonResponse({"msg":u"该用例不存在","status":3})
            else:
                if Case.objects.filter(name=case_name,api=case_api,is_deleted=0):
                    return JsonResponse({"msg":u"该用例已存在","status":2})
                case = Case()
            case.name = case_name
            case.user = request.user
            case.api = case_api
            case.headers = case_headers
            case.cookies = case_cookies
            case.validation = case_validation
            case.parameter = case_parameter
            case.encryption_type = case_encryption_type
            if case_tag_id!=0:
                case_tag=Tag.objects.get(id=int(case_tag_id))
                case.tag = case_tag
            try:
                case.save()
                return JsonResponse({"msg":u"保存用例成功","status":0})
            except Exception:
                return JsonResponse({"msg":u"保存用例失败","status":-1})

        else:
            return JsonResponse({"msg":u"校验失败","status":4})

@login_required
def get_testcases(request,api_id):
    if request.method == 'GET':
        api = Api.objects.filter(id=int(api_id),is_deleted=0)
        if api:
            apis = api[0].get_values("id", "name", "path", "method", "proj","description")
            return render(request,'api_testcase.html',{"api":apis})
        else:
            return render(request,'wrong.html')

@login_required
def get_caseslist(request):
    if request.method == 'GET':
        api_id = request.GET.get("id",'')
        if api_id is None:
            return render(request,'wrong.html')
        api = Api.objects.filter(id=int(api_id),is_deleted=0)
        if api:
            cases = [ i.get_values("id",'name','tag','headers','cookies','parameter','user','update_time','validation') for i in api[0].get_all_case().order_by('-update_time') ]
            return JsonResponse({"cases": cases})
        else:
            return render(request,'wrong.html')


# @login_required
def get_tags(request):
    return JsonResponse(dict(data=list(Tag.objects.filter(is_deleted=0).order_by("id").values('id','name'))))


@login_required
def get_case(request,case_id):
    if request.method != 'GET':
        return render(request,'wrong.html')
    case = Case.objects.filter(id=int(case_id),is_deleted=0)[0]
    if case:
        api = case.api
        tags = Tag.objects.filter(is_deleted=0).order_by("id")
        plainText = ''
        if case.parameter == '':
            para = json.loads('{}')
        else:
            try:
                para = json.loads(case.parameter)
            except ValueError:
                para = json.loads('{}')
                plainText = case.parameter
        para_count = len(para.keys())
        if case.headers == '':
            headers = json.loads('{}')
        else:
            headers = json.loads(case.headers)
        headers_count = len(headers.keys())
        if case.cookies == '':
            cookies = json.loads('{}')
        else:
            cookies = json.loads(case.cookies)
        cookies_count = len(cookies.keys())
        valids = case.validation
        counts={}
        counts["para_count"]=para_count
        counts["headers_count"]=headers_count
        counts["cookies_count"]=cookies_count

        return render(request,'api_testcase_edit.html',{"api":api,"tags":tags,"case":case,"counts":counts,"para":para,"headers":headers,"cookies":cookies,"valids":valids,"plainText":plainText})
    else:
        return render(request, 'wrong.html')


class CaseQueryView(View):
    def get(self,request):
        sortType = request.GET.get("sortType","desc")
        pj = request.GET.get("project","")
        kw = request.GET.get("kw","")
        page = request.GET.get('currPage',1)
        tag = request.GET.get('tag',"")
        api = request.GET.get('api',"")
        if pj!= "":
            proj = Proj.objects.get(id=int(pj))
            apis = Api.objects.filter(proj=proj,is_deleted=0)
            case_all = Case.objects.filter(api__in=apis,is_deleted=0)
        else:
            case_all = Case.objects.filter(is_deleted=0)
        # count = case_all.count()
        if sortType == 'desc':
            case_all = case_all.order_by("-update_time")
        elif sortType == 'asc':
            case_all = case_all.order_by("update_time")
        if tag != "":
            case_all = case_all.filter(tag=int(tag))
        if api != "":
            case_all = case_all.filter(api=int(api))
        if kw:
            case_all = case_all.filter(name__contains=kw)
        sum = case_all.count()
        low,high = get_slice(sum,int(page))
        cases = case_all[low:high]
        data1 = [ i.get_values('id','name','parameter','api','tag','user','update_time') for i in cases]
        return JsonResponse({"count":sum,"currentPage":page,"data":data1})


class CaseCopyView(LoginRequiredView,View):
    def get(self,request,case_id):
        return render(request,'wrong.html')

    def post(self,request,case_id):
        cases = Case.objects.filter(id=int(case_id))
        if not cases:
            return JsonResponse({"status":-1,"msg":"wrong case id"})
        case = cases[0]
        name = case.name+str(int(time.time()))
        if Case.objects.filter(name=name,is_deleted=0):
            return JsonResponse({"status":1,"msg":"try again later"})
        c = Case()
        c.name = name
        c.cookies = case.cookies
        c.headers = case.headers
        c.parameter = case.parameter
        c.encryption_type = case.encryption_type
        c.validation = case.validation
        c.api = case.api
        c.tag = case.tag
        c.user = request.user
        c.save()
        return JsonResponse({"status":0,"msg":"copy sucess"})


@login_required
def case_delete(request,case_id):
    if request.method == 'GET':
        return JsonResponse({"status":-1,"msg":"wrong request method"})
    cases = Case.objects.filter(id=int(case_id))
    if not cases:
        return JsonResponse({"status":1,"msg":"wrong case id"})
    case = cases[0]
    case.is_deleted = 1
    case.save()
    return JsonResponse({"status":0,"msg":"delete sucess"})

def get_users(request):
    if request.method != 'GET':
        return JsonResponse({"status":-1,"msg":u"请求方式错误！"})
    else:
        users = User.objects.all()
        return JsonResponse({"status":0,"data":list(users.values('id','username'))})
    
    
def get_env(request):
    env_all = runtime_env.objects.filter(is_deleted=0)
    # proj_id = int(request.GET.get('project','0'))
    # if proj_id == 0:
    #     envs = env_all
    # else:
    #     proj = Proj.objects.filter(id=proj_id)
    #     envs = env_all.filter(Proj=proj)
    plan_id = int(request.GET.get('planId','0'))
    if plan_id == 0:
        envs = env_all
    else:
        p = plan.objects.filter(id=plan_id)
        envs = envs.filter(Proj=p[0].proj)
    return JsonResponse(dict(envs=list(envs.values('id','name'))))

def upload_file(request): 
    if request.method == "POST":    # 请求方法为POST时，进行处理 
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None 
        if not myFile: 
            return JsonResponse({"status":-1,"msg":"no files for upload!"}) 
        if not myFile.name.endswith('.py'):
            return JsonResponse({"status":-1,"msg":"请输入py文件!"})
        destination = open(os.path.join(os.getcwd()+"/upload/",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作 
        current_file = open(os.path.join("/Users/tcxy/myproj/easyapi-1/upload/","currFile.py"),'wb+')
        currfile = os.path.join(os.getcwd()+'/upload/currFile.py')
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk) 
            current_file.write(chunk)
        destination.close() 
        current_file.close()
        reload(dealCase)
        iptApi = dealCase.ImportApi(request)
        try:
            if iptApi.initCases() == 0:
                # if os.path.exists(currfile):
                #     os.remove(currfile)
                return JsonResponse({"status":0,"msg":u"用例批量导入成功!"})
            else:
                return JsonResponse({"status":-1,"msg":u"用例批量导入失败!"})
        except:
            return JsonResponse({"status":2,"msg":"导入失败"})
