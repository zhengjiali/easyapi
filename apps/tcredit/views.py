# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
# from apilogger import apiLogger
from users.views import login_required
import logging
from utils.send_email import send_email
from time import sleep

logger = logging.getLogger("django")
# Create your views here.
#联通
Unicom = {"130","131","132","145","155","156","176","185","186"}
#移动
Mobile = {"134","135","136","137","138","139","150","151","152","157","158","159","182","183","184","187","178","188","147"}
#电信
Telecom = {"133","153","177","180","181","189"}
#xn_blackSelfhit
Black = {"13379233629","15811339686","12345678901","11111111111"}

# logger = apiLogger()

# @login_required
def test(request):
    sleep(10)
    data = {"status":0,"msg":"sucess"}
    logger.info('seccess requests-test')
    # logger.info(' %s %s (test) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    return JsonResponse(data)

def get_age(request):
    # logger.info(' %s %s (get_age) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    idcard = request.GET.get('idcard','')
    if not idcard.isdigit():
        return JsonResponse({"status":-1,"msg":"格式错误"})
    age = datetime.now().year - int(idcard[6:10])
    return JsonResponse({"status":0,"msg":"请求成功","data":{"age":age}})

def get_operator(request):
    logger.info(' %s %s (get_operator) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    phone = request.GET.get('phone','')
    if not phone.isdigit() or len(phone) != 11:
        return JsonResponse({"status":-1,"msg":"格式错误"})
    label = phone[0:3]
    if label in Unicom:
        return JsonResponse({"status":0,"msg":"请求成功","data":{"operator":"Unicom"}})
    elif label in Mobile:
        return JsonResponse({"status":0,"msg":"请求成功","data":{"operator":"Mobile"}})
    elif label in Telecom:
        return JsonResponse({"status":0,"msg":"请求成功","data":{"operator":"Telecom"}})
    else:
        return JsonResponse({"status":0,"msg":"请求成功","data":{"operator":"Unknown"}})

def check(request):
    logger.info(' %s %s (check) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    phone = request.GET.get('phone','')
    idcard = request.GET.get('idcard','')
    name = request.GET.get('name','')
    # if idcard == '' or name == '' or len(phone) != 11 or not phone.isdigit() or not idcard.isdigit():
    if name.isdigit():
        return JsonResponse({"status":-1,"msg":"格式错误"})
    else:
        return JsonResponse({"status":0,"msg":"请求成功"})


def get_data(request):
    logger.info(' %s %s (get_data) %s %s'%(request.method,request.path_info,request.user,request.environ["REMOTE_ADDR"]))
    idcard = request.GET.get('idcard','')
    phone = request.GET.get('phone','')
    name = request.GET.get('name','')
    if not phone.isdigit() or len(phone) != 11:
        return JsonResponse({"status":-1,"msg":"格式错误"})
    if not idcard.isdigit():
        return JsonResponse({"status":-1,"msg":"格式错误"})
    age = datetime.now().year - int(idcard[6:10])
    if phone in Black:
        xn_blackSelfhit = True
    else:
        xn_blackSelfhit = False
    xn_blackhit = False
    xn_age = age
    label = phone[0:3]
    if label in Unicom:
        xn_openToNowdays = 1
        xn_currentStatus = "正常"
        xn_gender = "男"
        xn_mobVerifyResult = 1
        xn_cardType = "信用卡"
        xn_idCardValid = 123
        xn_callTotalTime30Day = 1203
    elif label in Mobile:
        xn_openToNowdays = 2
        xn_currentStatus = "正常"
        xn_gender = "女"
        xn_mobVerifyResult = 1
        xn_cardType = "信用卡"
        xn_idCardValid = 55
        xn_callTotalTime30Day = 990

    elif label in Telecom:
        xn_openToNowdays = 3
        xn_currentStatus = "正常"
        xn_gender = "男"
        xn_mobVerifyResult = 1
        xn_cardType = "信用卡"
        xn_idCardValid = 234
        xn_callTotalTime30Day = 100


    else:
        xn_openToNowdays = 0
        xn_currentStatus = ""
        xn_gender = "女"
        xn_mobVerifyResult = -1
        xn_cardType = "信用卡"
        xn_idCardValid = 0
        xn_callTotalTime30Day = 0

    return JsonResponse({"status":0,"data":{"xn_blackSelfhit":xn_blackSelfhit,"xn_blackhit":xn_blackhit,
                                            "xn_age":xn_age,"xn_openToNowdays":xn_openToNowdays,
                                            "xn_currentStatus":xn_currentStatus,"xn_gender":xn_gender,
                                            "xn_mobVerifyResult":xn_mobVerifyResult,"xn_cardType":xn_cardType,
                                            "xn_idCardValid":xn_idCardValid,"xn_callTotalTime30Day":xn_callTotalTime30Day}})

def send(request):
    if send_email("zhengjiali2014@163.com","done"):
        return JsonResponse({"status":0})
    else:
        return JsonResponse({"status":-1})
