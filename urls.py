from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    (r'^account/', include('bhagirath.apps.account.urls')),
    (r'^documents/', include('bhagirath.apps.documents.urls')),
    ('^/?$', include('bhagirath.apps.base.urls')),
)
