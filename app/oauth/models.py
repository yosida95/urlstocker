from django.db import models


class RequestToken(models.Model):
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)

    def set_token(self, key, secret):
        self.key = key
        self.secret = secret


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)

    def set_id(self, id):
        self.id = id

    def set_token(self, key, secret):
        self.key = key
        self.secret = secret
