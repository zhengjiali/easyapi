# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2019/2/27 10:44 PM'
from random import Random
from django.core.mail import send_mail

from easyapi.settings import EMAIL_FROM


def send_email(email,send_type="done"):
    email_title = ""
    email_body = ""

    if send_type == "done":
        email_title = "任务完成"
        email_body = "任务完成"
        send_status = send_mail(subject=email_title,message=email_body,from_email=EMAIL_FROM,recipient_list=[email])
        if send_status:
            return True
        else:
            return False
    elif send_type == "forget":
        email_title = "重置密码"
        email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}".format(random_str)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            return True
        else:
            return False




def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str


