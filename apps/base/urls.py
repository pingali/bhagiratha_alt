#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.apps.base.views',
    (r'^/?$',                      'homepage'),
)
