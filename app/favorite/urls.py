#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'get_favorites', 'favorite.views.get_favorites'),
)
