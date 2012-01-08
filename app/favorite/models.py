#-*- coding: utf-8 -*-

from datetime import datetime
from django.db import models

from oauth.models import User


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField()

    def set_id(self, id):
        assert isinstance(id, int) or isinstance(id, long)
        self.id = id

    def set_text(self, text):
        assert isinstance(text, unicode)
        self.text = text

    def set_created_at(self, created_at):
        assert isinstance(created_at, datetime)
        self.created_at = created_at


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
