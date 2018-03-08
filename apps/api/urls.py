# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/2/26 下午10:33'
from django.conf.urls import url

from .views import ApiListView,ApiView,TestView,data_list,saveconf,apis_list,ApiConfListView,get_tags


urlpatterns = [
    url(r'^apis/$', apis_list),
    url(r'^(?P<api_id>\w+)/list/$',ApiConfListView.as_view()),
    url(r'^cases$',data_list),
    url(r'^(?P<api_id>\w+)/$',TestView.as_view(),name="test"),
    url(r'^$',ApiView.as_view(),name="addapi"),
    url(r'^\w+/testapi$',TestView.as_view()),
    url(r'\w+/saveconf$',saveconf),
    url(r'^tags$',get_tags)

]
