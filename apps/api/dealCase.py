# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.getcwd()+'/upload/')
import currFile
from .models import Api,Case,Proj
import pickle

class ImportApi:
    def __init__(self,request):
        reload(currFile)
        from upload.currFile import name,path,value
        self.user = request.user
        self.api = Api()
        self.api.name = name
        self.api.path = path
        self.api.method = 'POST'
        self.api.proj = Proj.objects.get(id=3)
        self.api.user = request.user
        self.value = value
    def initCases(self):
        try:
            self.api.save()
            for item in self.value:
                case = Case()
                case.name = item[0]
                case.user = self.user
                case.api = self.api
                case.headers = ''
                case.cookies = ''
                case.validation = item[4]
                case.parameter = item[2]
                case.encryption_type = 3
                case.save()
            return 0
        except Exception as e:
            return 1
