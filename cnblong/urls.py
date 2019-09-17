# -*- coding:UTF-8 -*-
__autor__ = 'zhouli'
__date__ = '2019/9/2 21:45'


from django.conf.urls import url
from .views import test

urlpatterns = [
    url(r'^test_url/$', test, name='test_url'),
    url(r'^test_urls/$', test),
]
