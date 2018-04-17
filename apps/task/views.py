# -*- coding=utf-8 -*-
from django.shortcuts import render
from models import *
from api.models import Case
from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.auth.models import User
from api.test_views import test_case,save_result
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


def save_task(plan_id):
    t = task()
    t.plan = plan.objects.get(id=int(plan_id))
    t.runtime_env = runtime_env.objects.get(id=1)
    t.status=0
    t.save()
    t.plan.task_count += 1
    t.plan.save()
    return t.id
    # return JsonResponse({"msg":'sucess','status':0})

def execute_task(task_id):
    try:
        t = task.objects.get(id=task_id)
        p = t.plan
        e = t.runtime_env
        for case in p.cases.all():
            r = test_case(e.id,case)
            save_result(r,case,task_id)
        t.status=1
        t.save()
        return t.status

    except Exception as e:
        return t.status

class TaskView(View):
    def post(self,request,plan_id):
        task_id = save_task(plan_id)
        status = execute_task(task_id)
        return JsonResponse({"status":status})