"""easyapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
# from django.contrib import admin
from users.views import LoginView,LogoutView
from api.views import get_projects,get_users,get_env,upload_file
from task.report import get_tasks,task_query,get_report,get_cases,get_result
from task.statistics import CountView
import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^api/',include("api.urls",namespace='api')),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^projs/$',get_projects),
    url(r'^plan/',include("task.urls",namespace='plan')),
    url(r'^users/$',get_users),
    url(r'^env/$',get_env),
    url(r'^task/$',get_tasks),
    url(r'^task/query$',task_query),
    url(r'^task/(?P<task_id>\w+)/report$',get_report),
    url(r'^task/(?P<task_id>\w+)/cases$',get_cases),
    url(r'^task/(?P<task_id>\w+)/cases/(?P<case_id>\w+)$',get_result),
    url(r'^statistics/$',CountView.as_view()),
    url(r'^tcredit/',include("tcredit.urls",namespace='tcredit')),
    url(r'^uploadFile$',upload_file),

]

# from django.conf.urls import url,include
# from rest_framework import routers
# from .viewsets import TagViewset,UserViewset,ApiConfigViewset
#
# router = routers.DefaultRouter()
#
# router.register(r'tags',TagViewset)
# router.register(r'apis',ApiConfigViewset)
# router.register(r'users',UserViewset)
#
# urlpatterns = [
#     url(r'^',include(router.urls)),
#     url(r'^api/',include('rest_framework.urls',namespace='rest_framework')),
# ]
