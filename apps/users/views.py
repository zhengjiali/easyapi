# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponseRedirect


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            name = request.POST.get("username","")
            passwd = request.POST.get("password","")
            user = authenticate(username=name,password=passwd)
            if user is not None:
                login(request, user)
                return render(request, "test.html",{"user":user})
            else:
                return render(request, "login.html", {"login_form": login_form, "msg": u"用户名密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('login'))