# -*- coding:utf-8 -*-


import xadmin
from xadmin import views

from .models import *

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "XXXX公司"
    menu_style = "accordion"

class TagAdmin(object):
    list_display = ['name','father_id','create_time']
    search_fields = ['name','father_id','create_time']
    list_filter = ['name','father_id','create_time']

class ApiAdmin(object):
    list_display = ['path','method','name','description','tag','user']
    search_fields = ['path','method','name','description','tag','user']
    list_filter = ['path','method','name','description','tag','user']

class ValidationAdmin(object):
    list_display = ['key','value','api_id']
    search_fields = ['key','value','api_id']
    list_filter = ['key','value','api_id']

class ApiConfAdmin(object):
    list_display = ['name','parameter','api','character']
    search_fields = ['name','parameter','api','character']
    list_filter = ['name','parameter','api','character']

class CharacterAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(Api,ApiAdmin)
xadmin.site.register(Validation,ValidationAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(ApiConf,ApiConfAdmin)
xadmin.site.register(Character,CharacterAdmin)
