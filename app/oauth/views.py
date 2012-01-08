#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings
import tweepy

from . import login as oauth_login, get_oauth_handler
from .models import RequestToken, User


def login(request):
    oauth = get_oauth_handler()
    redirect = oauth.get_authorization_url(True)

    try:
        RequestToken.objects.create(
            key=oauth.request_token.key, secret=oauth.request_token.secret)
    except:
        pass

    return HttpResponseRedirect(redirect)


def authenticate(request):
    redirect = settings.FAILED_LOGIN

    request_key = request.REQUEST.get('oauth_token', '')
    verifier = request.REQUEST.get('oauth_verifier', '')

    try:
        request_token = RequestToken.objects.get(key=request_key)
    except RequestToken.DoesNotExist:
        pass
    else:
        oauth = get_oauth_handler()
        oauth.set_request_token(request_token.key, request_token.secret)
        request_token.delete()

        try:
            oauth.get_access_token(verifier)
            user_id = tweepy.API(auth_handler=oauth).me().id

            q = User.objects.filter(id=user_id)
            if 0 < q.count():
                user = q[0]
            else:
                user = User()
                user.set_id(user_id)

            user.set_token(oauth.access_token.key,
                                  oauth.access_token.secret)
            user.save()

        except tweepy.TweepError:
            pass
        else:
            oauth_login(request, user)
            redirect = settings.SUCCESS_LOGIN

    return HttpResponseRedirect(redirect)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(settings.HOMEPAGE)
