# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/8/20 下午10:32'

from db import DBAdapter
from django.views.generic.base import View
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.http import JsonResponse


class CountView(View):
    def get(self,request):
        return render(request,'statistics.html')

    def post(self,request):
        result = {}
        planId = request.POST.get('planId','')
        time = request.POST.get('time','')
        if planId != '':
            if time != '':
                sql = "select response from api_result where url like '%"+planId+"%' and response like '%接口调用成功%' and create_time > '"+time+"'"
            else:
                sql = "select response from api_result where url like '%"+planId+"%' and response like '%接口调用成功%'"

            db = DBAdapter()
            fields = db.ext(sql)
            for field in fields:
                try:
                    data = json.loads(field[0])
                    v = data["data"]
                    for item in v:
                        if not result.has_key(item):
                            result[item] = {}
                            result[item]["__total__"]=0

                        if v[item].has_key('value'):
                            result[item]["__total__"] += 1
                            value = str(v[item]["value"])
                            if not result[item].has_key(value):
                                result[item][value] = 1
                            else:
                                result[item][value] += 1
                except:
                    continue
        return JsonResponse({"status":0,"data":result})




