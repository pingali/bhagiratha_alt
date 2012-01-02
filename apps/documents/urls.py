#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhagirath.apps.documents.views',
       (r'^$',    'index'),
       (r'^new$',    'new'),
       (r'^show/(?P<doc_id>\d+)/?$',    'show'),
       (r'^edit/(?P<doc_id>\d+)/?$',    'edit'),
       (r'^delete/(?P<doc_id>\d+)/?$',  'delete'),
       (r'^assign/(?P<doc_id>\d+)/?$',  'assign'),
       (r'^unassign/(?P<doc_id>\d+)/?$',  'unassign'),
)
