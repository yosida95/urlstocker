#-*- coding: utf-8 -*-

import tweepy
import re

from oauth import login_required, get_oauth_handler, get_user
from .models import URL, URLProcess, Tweet, Favorite


@login_required
def get_favorites(request):
    user = get_user(request)

    oauth = get_oauth_handler()
    oauth.set_access_token(user.key, user.secret)
    api = tweepy.API(auth_handler=oauth)

    q_fav = Favorite.objects.filter(user=user)
    p = re.compile(r'https?:\/\/')

    for favorite in favorites(api, user.id):
        if not p.search(favorite.text):
            continue

        q_tweet = Tweet.objects.filter(id=favorite.id)
        if 0 < q_tweet.count():
            tweet = q_tweet[0]
        else:
            tweet = Tweet()
            tweet.set_id(favorite.id)
            tweet.set_text(favorite.text)
            tweet.set_created_at(favorite.created_at)
            tweet.save()

            for url in tweet.pick_urls():
                _url = URLProcess(url)
                _url.process()
                q = URL.objects.filter(url=_url.get_url())

                if 0 < q.count():
                    url = q[0]
                else:
                    url = URL()
                    url.set_url(_url.get_url())
                    url.set_title()
                    url.save()

                tweet.urls.add(url)
                tweet.save()

        if q_fav.filter(tweet=tweet).count() < 1:
            fav = Favorite()
            fav.set_user(user)
            fav.set_tweet(tweet)
            fav.save()
        else:
            break


def favorites(api, user_id):
    assert isinstance(api, tweepy.API)
    assert isinstance(user_id, int) or isinstance(user_id, long)

    page = 1
    iscontinue = True
    favorites = api.favorites(user_id, page)

    while iscontinue:
        for favorite in favorites:
            yield favorite
        else:
            page += 1
            favorites = api.favorites(user_id, page)
            iscontinue = True if 0 < len(favorites) else False
