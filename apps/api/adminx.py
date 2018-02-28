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

class ApiConfigAdmin(object):
    list_display = ['path','method','name','parameter','description','tag','user']
    search_fields = ['path','method','name','parameter','description','tag','user']
    list_filter = ['path','method','name','parameter','description','tag','user']

class ValidationAdmin(object):
    list_display = ['key','value','api_id']
    search_fields = ['key','value','api_id']
    list_filter = ['key','value','api_id']


xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(ApiConfig,ApiConfigAdmin)
xadmin.site.register(Validation,ValidationAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)