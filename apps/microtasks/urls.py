#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.apps.microtasks.views',
       (r'^$',    'index'),
       (r'^show/(?P<mtask_id>\d+)/?$',    'show'),
       (r'^edit/(?P<mtask_id>\d+)/?$',    'edit'),
       (r'^reassign/(?P<mtask_id>\d+)/?$',  'reassign')

)
