#-*- coding: utf-8 -*-

SESSION_KEY = '_twitter_logged_in'

from django.http import HttpResponseRedirect
from django.conf import settings
from .models import User


def login(request, user):
    assert isinstance(user, User)

    request.session[SESSION_KEY] = user.id


def is_logged_in(request):
    if SESSION_KEY in request.session and request.session[SESSION_KEY]:
        return True

    return False


def login_required(function):
    def _view_func(request, *args, **keyargs):
        if is_logged_in(request):
            return function(request, *args, **keyargs)
        return HttpResponseRedirect(settings.LOGIN_URL)
    return _view_func
