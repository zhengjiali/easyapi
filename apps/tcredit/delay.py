# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__filename__ = 'delay.py'
__date__ = '2018/12/10 下午4:32'

from apilogger import apiLogger
from django.http.response import JsonResponse
from time import sleep

logger = apiLogger()

def delay10s(request):
    print 'start'
    logger.info(' %s %s (delay10s-start) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    sleep(10)
    print 'end'
    logger.info(' %s %s (delay10s-end) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    return JsonResponse({"status":0,"msg":"sucess"})