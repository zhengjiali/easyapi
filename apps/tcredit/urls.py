from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'test$',test),
    url(r'getAge',get_age),
    url(r'getOperator',get_operator),
    url(r'check',check),
    url(r'getData',get_data),
]