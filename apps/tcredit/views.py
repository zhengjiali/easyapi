# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime


# Create your views here.
#联通
Unicom = {"130","131","132","145","155","156","176","185","186"}
#移动
Mobile = {"134","135","136","137","138","139","150","151","152","157","158","159","182","183","184","187","178","188","147"}
#电信
Telecom = {"133","153","177","180","181","189"}
#xn_blackSelfhit
Black = {"13379233629","15811339686","12345678901","11111111111"}

def test(request):
    data = {"status":0,"msg":"sucess"}
    return JsonResponse(data)

def get_age(request):
    idcard = request.GET.get('idcard','')
    if not idcard.isdigit():
        return JsonResponse({"status":-1,"msg":"格式错误"})
    age = datetime.now().year - int(idcard[6:10])
    return JsonResponse({"status":0,"msg":"请求成功","data":{"age":age}})

def get_operator(request):
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
    phone = request.GET.get('phone','')
    idcard = request.GET.get('idcard','')
    name = request.GET.get('name','')
    # if idcard == '' or name == '' or len(phone) != 11 or not phone.isdigit() or not idcard.isdigit():
    if name.isdigit():
        return JsonResponse({"status":-1,"msg":"格式错误"})
    else:
        return JsonResponse({"status":0,"msg":"请求成功"})


def get_data(request):
    '''
        xn_blackSelfhit(xn自有黑名单),
        xn_blackhit(xn第三方黑名单),
        xn_age(xn年龄),
        xn_openToNowdays(xn手机号码在网时长),
        xn_currentStatus(xn手机号码当前状态),
        xn_gender(xn性别),
        xn_mobVerifyResult(xn手机实名验证结果),
        xn_threeFactorVerificaiton(xn银行卡三要素验证结果),
        xn_cardType(xn银行卡类型),
        xn_idCardValid(xn证件有效期),
        xn_callTotalTime30Day(xn近30天通话总时长)
    '''
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
