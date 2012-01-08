#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'login', 'oauth.views.login'),
    url(r'authenticate', 'oauth.views.authenticate'),
    url(r'logout', 'oauth.views.logout'),
)
