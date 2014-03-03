#!/usr/bin/python
# -*- coding: utf-8 -*-

from boto.s3.bucket import Bucket
from ssg.SSGInterface.bucket import SSGBucket
from ssg.SSGClient.fruit import Fruit


class Tree(object):

    def __init__(self, connection=None, name=None, real_bucket_name=None, fruit_class=Fruit):
        self.ssg_bucket = SSGBucket(connection.ssg_conn, name, real_name=real_bucket_name)
        self.s3_bucket = Bucket(connection.s3_conn, real_bucket_name)
        self.name = name
        self.connection = connection
        self.fruit_class = fruit_class

    def new_fruit(self, fruit_name=None):
        if not fruit_name:
            raise ValueError('Empty fruit names are not allowed')
        return self.fruit_class(self, fruit_name)

    def get_fruit(self, fruit_name, validate=True):
        ssg_key = self.ssg_bucket.get_key(fruit_name, validate)
        fruit = self.fruit_class(self, name=fruit_name, ssg_key=ssg_key)
        return fruit

    def get_location(self):
        return self.ssg_bucket.get_location()

    def list(self):
        return self.ssg_bucket.list()

    def get_fruit_list(self):
        fruit_object_list = list()
        fruit_list = self.list()

        for f in fruit_list:
            fruit = self.get_fruit(f)
            fruit_object_list.append(fruit)
        return fruit_object_list

    def lookup(self, fruit_name):
        return self.get_fruit(fruit_name)

    def set_fruit_class(self, fruit_class):
        self.fruit_class = fruit_class