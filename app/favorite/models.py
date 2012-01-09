#-*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
import re
from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlopen, urlencode
from BeautifulSoup import BeautifulSoup

from oauth.models import User


class URLProcess(object):

    def __init__(self, url):
        self.set_url(url)

    def set_url(self, url):
        assert isinstance(url, unicode) or isinstance(url, str)
        self.url = url

    def get_url(self):
        return self.url

    def expand(self, url):
        uxnu_query = urlencode([('format', 'plain'), ('url', url)])
        uxnu = urlunparse(['http', 'ux.nu', '/hugeurl', '', uxnu_query, ''])
        expanded = urlopen(uxnu).read()
        return expanded if expanded else url

    def process(self):
        _url = urlparse(self.expand(self.url))

        scheme = self.process_scheme(_url[0])
        netloc = self.process_netloc(_url[1])
        path = self.process_path(_url[2])
        parms = self.process_parms(_url[3])
        query = self.process_query(_url[4])
        fragment = self.process_fragment(_url[5])

        self.url = urlunparse([scheme, netloc, path, parms, query, fragment])

    def process_scheme(self, scheme):
        return scheme

    def process_netloc(self, netloc):
        return netloc

    def process_path(self, path):
        return path

    def process_parms(self, parms):
        return parms

    def process_query(self, query):
        if query:
            query = urlencode(parse_qsl(query).sort())
        return query

    def process_fragment(self, fragment):
        return fragment


class URL(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=datetime.utcnow)

    def set_url(self, url):
        assert isinstance(url, str) or isinstance(url, unicode)

        self.url = url

    def set_title(self, title=None):
        if not title:
            try:
                soup = BeautifulSoup(urlopen(self.url).read())
                title = soup.title.text
            except:
                title = ''

        self.title = title


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField()
    urls = models.ManyToManyField(URL, related_name='tweets')

    def set_id(self, id):
        assert isinstance(id, int) or isinstance(id, long)
        self.id = id

    def set_text(self, text):
        assert isinstance(text, unicode)
        self.text = text

    def set_created_at(self, created_at):
        assert isinstance(created_at, datetime)
        self.created_at = created_at

    def pick_urls(self):
        return re.findall(r'https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+',
                          self.text)

    def add_url(self, url):
        self.urls.add(url)


class Tag(models.Model):
    name = models.CharField(max_length=140)

    def set_name(self, name):
        assert isinstance(name, unicode)
        self.name = name


class Favorite(models.Model):
    user = models.ForeignKey(User)
    tweet = models.ForeignKey(Tweet)
    tags = models.ManyToManyField(Tag, related_name='favorites')

    def set_user(self, user):
        assert isinstance(user, User)
        self.user = user

    def set_tweet(self, tweet):
        assert isinstance(tweet, Tweet)
        self.tweet = tweet

    def add_tag(self, tag):
        assert isinstance(tag, Tag)
        self.tags.add(tag)
