#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.apps.translations.views',
       (r'^$',    'index'),
       (r'^show/(?P<translation_id>\d+)/?$',    'show'),
       (r'^edit/(?P<translation_id>\d+)/?$',    'edit'),
       (r'^languages/?$',                       'languages'),
       
)
