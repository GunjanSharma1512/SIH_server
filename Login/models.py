# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.email

    def as_json(self):
        return dict(
            name=self.name,
            email=self.email,
            password=self.password,
        )

class Image(models.Model):
    picture = models.CharField(max_length=200)
    hash_code = models.CharField(max_length=200)
    encrypted_code = models.CharField(max_length=200)

    def as_json(self):
        return dict(
            picture=self.picture,
            hash_code=self.hash_code,
            encrypted_code=self.encrypted_code,
        )
