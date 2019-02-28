from django.conf.urls import url
from views import *
from delay import *


urlpatterns = [
    url(r'test$',test),
    url(r'getAge',get_age),
    url(r'getOperator',get_operator),
    url(r'check',check),
    url(r'getData',get_data),
    url(r'delay10s',delay10s),
    url(r'sendmail',send),
]