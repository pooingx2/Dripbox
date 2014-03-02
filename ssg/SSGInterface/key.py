#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path
from urllib2 import quote
import json

from ssg.common import utils
from ssg.common.exceptions import *


class SSGKey:
    def __init__(self, bucket=None, name=None, real_name=None):
        self.bucket = bucket
        self.name = name

        self.filename = None
        self.filepath = None
        self.type = None
        self.modified_by = None
        self.created_by = None
        self.owned_by = None
        self.size = None
        self.size_ssg = None
        self.url = None

        #upload body
        self.policy = None
        self.AWSAccessKeyId = None
        self.signature = None
        self.key = None
        self.x_amz_storage_class = None

        #related with user_s3
        self.real_name = real_name
        self.size_s3 = None
        self.id = None

        self.key_path = self._make_key_path()

    def _make_key_path(self):
        key_path = utils.get_utf8_value(self.name)
        return key_path

    def exists(self):
        """
        Returns True if the key exists

        :rtype: bool
        :return: Whether the key exists on S3
        """
        return bool(self.bucket.lookup(self.name))

    def get_metadata(self):
        return self.__dict__

    def get_contents_to_filename(self, filename):
        method = "GET"
        url = self.url
        response, content = self.bucket.connection.make_request(method, url, file_io=True)

        try:
            utils.check_response(response)
            with open(filename, 'wb') as f:
                f.write(content)
        except request_error as re:
            self.bucket.connection.request_error_handler(re, 'get_contents_to_filename',
                                                         method, url, response)

    def set_contents_from_filename(self, filename, size_s3):
        method = "POST"
        url = "buckets"
        self.filepath = filename
        self.size_ssg = path.getsize(self.filepath)
        self.size_s3 = size_s3
        self.size = self.size_s3 + self.size_ssg
        self.filename = filename
        request_param = {'name': self.name, 'size': self.size,
                         'size_s3': self.size_s3, 'size_ssg': self.size_ssg}

        response, content = self.bucket.connection.make_request(method, url,
                                                                bucket=self.bucket.name,
                                                                key=self.name,
                                                                body=request_param)
        try:
            utils.check_response(response)
            self.set_metadata(content)

        except request_error as re:
            self.bucket.connection.request_error_handler(re, 'set_contents_from_filename',
                                                         method, url, response,
                                                         bucket=self.bucket.name, key=self.name)
        return self.size

    def send_file(self):

        parameters = {'AWSAccessKeyId': self.AWSAccessKeyId, 'policy': self.policy,
                      'key': self.key, 'signature': self.signature, 'x-amz-storage-class': self.x_amz_storage_class}

        self._send_file_internal(parameters)
        self._finish_response()

    def generate_url(self):
        return self.url

    def set_metadata(self, content):
        data = json.loads(content)
        return self._set_metadata_internal(data)

    def _set_metadata_internal(self, metadata):
        self.id = metadata['id']
        self.created_by = metadata['created_by']
        self.modified_by = metadata['modified_by']
        self.owned_by = metadata['owned_by']
        self.real_name = metadata['storage_path_ssg']
        #self.name = metadata['path']
        #print "in set_metadata_internal : " + self.name

        upload_info = metadata['upload_info']
        self.policy = upload_info['policy']
        self.AWSAccessKeyId = upload_info['AWSAccessKeyId']
        self.key = upload_info['key']
        self.signature = upload_info['signature']
        self.x_amz_storage_class = upload_info['x-amz-storage-class']
        self.url = upload_info['upload_url']

    def _finish_response(self):
        method = "POST"
        url = "buckets"
        bucket_name = self.bucket.name
        query = "/key_finish?path="+quote(self.name)

        request_param = {"storage_path_s3": self.real_name, "bucket_s3": self.bucket.real_name}
        print str(type(self.real_name)) + "     " + str(type(self.bucket.real_name))
        response, content = self.bucket.connection.make_request(method, url, body=request_param,
                                                                bucket=bucket_name, query=query)
        try:
            utils.check_response(response)
            data = json.loads(content)
            #데이터 형식 확인 후 key_list return
            print 'data : ' + str(data)

        except request_error as re:
            self.bucket.connection.request_error_handler(re, 'finish_response', method, url,
                                                         response, bucket=bucket_name, query=query)
        return True

    def _send_file_internal(self, parameters):
        import pycurl

        c = pycurl.Curl()
        c.setopt(c.POST, 1)

        c.setopt(c.URL, str(self.url))
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.MAXREDIRS, 3)

        values = []

        for k, v in parameters.iteritems():
            if isinstance(k, unicode):
                k = k.encode("utf-8")
            if isinstance(v, unicode):
                v = v.encode("utf-8")
            values.append((k, v))

        values.append(("file", (pycurl.FORM_FILE, self.filepath)))
        print values
        c.setopt(c.HTTPPOST, values)
        c.setopt(c.SSL_VERIFYHOST, False)
        c.setopt(c.SSL_VERIFYPEER, False)
        c.perform()
        c.close()
