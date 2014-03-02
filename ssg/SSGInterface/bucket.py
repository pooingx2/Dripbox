#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from key import SSGKey
from ssg.common import utils
from ssg.common.exceptions import *


class SSGBucket:
    def __init__(self, connection=None, name=None, real_name=None, key_class=SSGKey):
        self.connection = connection
        self.name = name
        self.key_class = key_class
        self.real_name = real_name

    def new_key(self, key_name=None):
        key = self.key_class(self, key_name)
        return key

    def get_location(self):
        response, content = self.connection.make_request("GET", "buckets", bucket=self.name)
        location = utils.make_select_list(content, 'location')
        return location

    def generate_url(self):
        return self.connection._generate_path('buckets', bucket=self.name)

    def list(self):
        key_list = []
        method = "GET"
        url = "buckets"
        query = '/key_list?path=/'

        response, content = self.connection.make_request(method, url, bucket=self.name, query=query)
        try:
            utils.check_response(response)
            #데이터 형식 확인 후 key_list return
            key_list = utils.make_select_list(content, "path")

        except request_error as re:
            self.connection.request_error_handler(re, 'get_key_list', method, url,
                                                  response, bucket=self.name)
        return key_list

    def get_all_key(self):
        key_object_list = list()
        key_list = self.list()
        for k in key_list:
            key = self.get_key(k)
            key_object_list.append(key)
        return key_object_list

    def get_key(self, key_name, validate=True):
        """
        Returns a Key instance for an object in this bucket.

        :type key_name: string
        :param key_name: The name of the key to retrieve

        :rtype: :class:'ssg.SSGInterface.key.SSGKey'
        :returns: A Key object from this bucket.
        """
        method = "GET"
        url = "buckets"
        key = None
        response, content = self.connection.make_request(method, url, bucket=self.name,
                                                         key=key_name)

        try:
            utils.check_response(response)
            key = self._get_key_internal(self.key_class(self, key_name), content)

        except request_error as re:
            print "in get_key : " + str(content)
            if not validate is True:
                self.connection.request_error_handler(re, 'get_key', method, url,
                                                      response, bucket=self.name, key=key_name)
            key = SSGKey(self, name=key_name)

        return key

    # def copy_key(self, new_key_name, src_bucket_name,
    #              src_key_name, metadata=None):

    def _get_key_internal(self, key, content):
        """

        :type key:
        :param key:

        :type content:
        :param content:

        :rtype:
        :return:
        """
        data = json.loads(content)
        key.url = data['download_url']
        key.id = data['id']
        key.created_by = data['created_by']
        key.modified_by = data['modified_by']
        key.owned_by = data['owned_by']
        key.real_name = data['storage_path_s3']
        key.size_ssg = data['size_ssg']
        key.size_s3 = data['size_s3']
        key.size = data['size']

        print "in get_key_internal : " + key.real_name
        return key

    def new_key(self, key_name=None):
        """
        Create a new key

        :type key_name: string
        :param key_name: The name of the new key
        """
        if not key_name:
            raise ValueError('Empty key names are not allowed')
        return self.key_class(self, key_name)

    def set_key_class(self, key_class):
        """
        Set the Key class associated with this Bucket.

        :type key_class: class
        :param key_class: A subclass of Key that can be more specific
        """
        self.key_class = key_class
        return key_class.real_name

    def lookup(self, key_name):
        """
        Deprecated: Please use get_key method.

        :type key_name: string
        :param key_name: The name of the key to retrieve

        :rtype: :class:`ssg.SSGInterface.key.SSGKey`
        :returns: A Key object from this bucket.
        """
        return self.get_key(key_name)