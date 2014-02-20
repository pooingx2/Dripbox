__author__ = 'PJY'

from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    pwd = models.CharField(max_length=20)
    #pwd = models.CharField(max_length=200, blank=True, null=True)


class File(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    parent = models.CharField(max_length=20)
    user = models.ForeignKey(User)