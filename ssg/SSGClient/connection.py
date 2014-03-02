#!/usr/bin/python
# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
from boto.s3.cors import CORSConfiguration

from ssg.SSGClient.credential import Credential
from ssg.SSGClient.tree import Tree
from ssg.SSGInterface.connection import SSGConnection


class Connection(object):
    user_bucket_name = None

    def __init__(self, key_file=None, tree_class=Tree):
        if not (key_file is None):
            self.connection(key_file)

        else:
            self.s3_conn = S3Connection()
            self.ssg_conn = SSGConnection()

        self.tree_class = tree_class

    def connection(self, key_file, tree_class=Tree):
        #추후 수정 필요
        self._cre = Credential(key_file)
        self.s3_conn = S3Connection(self._cre.accessid, self._cre.secret)
        self.ssg_conn = SSGConnection(self._cre.group_key)
        self.tree_class = tree_class

    def create_tree(self, tree_name, headers=None, location='', policy=None):
        """
        create tree by bucket_name. return tree class

        :type tree_name: string
        :param tree_name: The name of the new tree

        :type location: str
        :param location: The location of the new bucket. You can use one of the
            constants in :class: ssg.SSGInterface.connection.Location
        """
        ssg_bucket = self.ssg_conn.create_bucket(tree_name, location)
        real_bucket_name = ssg_bucket.real_name
        if self.s3_conn.lookup(real_bucket_name) is None:
            self._create_user_s3_bucket_internal(real_bucket_name, location)
        else:
            #바로 이전거 delete 요청...
            print "you have already owned bucket : %s" % self.user_bucket_name
            return None

        tree = self.tree_class(self, tree_name, real_bucket_name)
        return tree

    # def delete_bucket(self, bucket_name, headers=None):
    #     #교범이 한테 real_bucket_name 받아와야 함
    #     #없을 경우에 api response에 따라 여기서 예외 처리....
    #     #real_bucket = ssg_conn.get_real_bucket_name(bucket_name)
    #     if real_bucket == None:
    #         print "you have not owned bucket : %s"%(bucket_name)
    #         return False
    #     else:
    #         bucket = self.s3_conn.lookup(real_bucket)
    #         self.s3_conn.delete(bucket, headers)
    #         self.ssg_conn.delete(bucket_name)
    #         return True

    def get_tree(self, tree_name, validate=True):
        """
        get tree by bucket_name.
        return tree class

        :type tree_name: string
        :param tree_name: The name of the new tree

        """
        ssg_bucket = self.ssg_conn.get_bucket(tree_name, validate)
        tree = self.tree_class(self, tree_name, ssg_bucket.real_name)

        return tree

    def get_all_trees(self):
        """
        get all trees in same group.
        return available tree list

        """
        tree_list = []
        ssg_bucket_list = self.ssg_conn.get_all_buckets()
        print ssg_bucket_list
        for ssg_bucket in ssg_bucket_list:
            tree_list.append(self.tree_class(self, ssg_bucket.name, ssg_bucket.real_name))
        return tree_list

    def lookup(self, tree_name):
        """

        """
        tree = self.get_tree(tree_name)
        return tree

    def set_tree_class(self, tree_class):
        """
        Set the Bucket class associated with this tree. If you want to subclass that
        for some reason this allows you to associate your new tree class.

        :type tree_class: class
        :param tree_class: A subclass of Tree that can be more specific
        """
        self.tree_class = tree_class

    def _create_user_s3_bucket_internal(self, real_bucket_name, location=None):
        method_list = ['PUT', 'POST', 'DELETE', 'GET', 'HEAD']
        new_bucket = self.s3_conn.create_bucket(real_bucket_name, location=location)
        cors_cfg = CORSConfiguration()
        cors_cfg.add_rule(method_list, allowed_origin=['*'], allowed_header=['*'])
        new_bucket.set_cors(cors_cfg)
