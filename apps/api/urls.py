# -*- coding:utf-8 -*-
__author__ = 'zhengjiali'
__date__ = '2018/2/26 下午10:33'
from django.conf.urls import url

from .views import *
from .test_views import CaseTestView

urlpatterns = [
    url(r'^apis$', ApiQueryView.as_view(),name="query" ),
    url(r'^(?P<api_id>\w+)/addCase$',CaseNewView.as_view(),name="addcase"),
    url(r'(?P<api_id>\w+)/cases/$',get_api_cases),
    url(r'^cases$',data_list),
    url(r'^(?P<api_id>\w+)$',ApiView.as_view(),name="api"),
    url(r'^addApi/$',ApiNewView.as_view(),name="addapi"),
    url(r'^cases/(?P<case_id>\w+)/doTest$',CaseTestView.as_view(),name="doTest"),
    url(r'^tags/$',get_tags)

]
