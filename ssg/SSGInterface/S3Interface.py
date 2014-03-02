#!/usr/bin/python
# -*- coding: utf-8 -*-

from boto.s3.connection import Location, S3Connection
from boto.s3.bucket import Bucket


class s3_interface:
    _bucket = None
    _bucket_dict = dict()

    def __init__(self, access_id='None', secret='None'):
        self.conn = S3Connection(access_id, secret)

    #S3에 연결
    #para :
    def connection(self, access_id, secret):
        #추후 수정 필요
        self.conn = S3Connection(access_id, secret)

    #버킷을 해당 이름으로 생성
    def create_bucket(self, bucket_name, headers=None, location='', policy=None):
        self.conn.create_bucket(bucket_name, headers, location, policy)

    #모든 버킷 리스트 불러오기
    def get_all_buckets(self, headers=None):
        return self.conn.get_all_buckets(headers)

    #버킷 이름으로 버킷 클래스 얻어오기
    def _get_bucket(self, bucket_name, validate=True, headers=None):
        bucket = self.conn.lookup(bucket_name, validate, headers)
        if bucket == None:
            print 'there is no bucket_name : %s'%(bucket_name)
            return False
        return bucket

    #버킷 이름으로 해당 버킷을 삭제하기.
    #삭제 실패시 False, 성공시 True
    def delete_bucket(self, bucket_name, validate=True, headers=None):
        bucket = self._get_bucket(bucket_name, validate, headers)
        if bucket == None:
            return False
        self.conn.delete_bucket(bucket, headers)
        return True

    #버킷에 대한 모든 정보 이름으로 탐색하여 받아오기
    #def get_bucket_info(self, bucket_name, validate=True, headers=None):
    #    bucket = self.conn.lookup(bucket_name, validate, headers)

    #버킷 이름과 키 이름으로 키 클래스 얻어오기(다운로드시 사용)
    def _get_key(self, bucket_name, key_name,
                bucket_headers=None, bucket_validate=None, key_headers=None):
        self._bucket = bucket_name
        self.bucket
        #bucket = self._get_bucket(bucket_name, bucket_validate, bucket_headers)
        if bucket == False:
            return False
        else :
            key = bucket.lookup(key_name, key_headers)
            if key == None:
                print 'there is no key_name : %s in bucket : %s'%(key_name, bucket_name)
                return False
            return key



    #해당 버킷에 해당 파일 업로
    # def set_contents_from_name(self,file_name, headers=None, replace=True, cb=None, num_cb=10,
    #                            policy=None, md5=None, reduced_redundancy=False, query_args=None,
    #                            encrypt_key=False, size=None, rewind=False):
    #










