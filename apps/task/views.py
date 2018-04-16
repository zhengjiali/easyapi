# -*- coding=utf-8 -*-
from django.shortcuts import render
from models import plan
from api.models import Case
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.views import login_required,LoginRequiredView

# Create your views here.

def new_plan(request):
    if request.method == 'GET':
        return JsonResponse({"msg":u"请求方式错误","status":"-1"})
    name = request.POST.get('name','')
    if name == '':
        return JsonResponse({"msg": u"名称不能为空", "status": "1"})
    elif plan.objects.filter(name=name):
        return JsonResponse({"msg":u"名称重复","status":2})
    desp = request.POST.get("description",'')
    p = plan()
    p.user = User.objects.get(id=1)
    p.name = name
    p.desp = desp
    p.save()
    case_list = request.POST.get("cases",'')
    if case_list != '':
        l = eval(case_list)
        for c in l:
            try:
                p.cases.add(Case.objects.get(id=c))
            except Exception:
                continue
    return JsonResponse({"msg":"sucess","status":0})



def get_plan(request,plan_id):
    try:
        p = plan.objects.get(id=int(plan_id),is_deleted=0)
        cases = p.get_cases()
        if p:
            return JsonResponse({"plan":p.get_values("name","description","user","task_count","create_time"),"cases":cases})
    except Exception as e:
        return JsonResponse({"msg":e.message,"status":0})