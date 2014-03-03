#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path, mkdir
from shutil import rmtree
from boto.s3.key import Key
from ssg.SSGClient.encryption import Encryption
# from ssg.SSGInterface.key import SSGKey


class Fruit(object):
    _tmp_dir = None

    def __init__(self, tree=None, name=None, ssg_key=None):
        self.tree = tree
        self.name = name

        if not ssg_key is None:
            self.ssg_key = ssg_key
            self.s3_key = Key(self.tree.s3_bucket, ssg_key.real_name)
        else:
            self.ssg_key = None
            self.s3_key = None

    def __unicode__(self):
        return self._tmp_dir

    def get_metadata(self):
        return self.ssg_key.get_metadata()

    def get_contents_to_file(self, fp, headers=None, num_cb=10, torrent=False, version_id=None,
                             res_download_handler=None, response_headers=None):
        #download file by using file pointer
        pass

    def get_contents_to_buf(self):
        #download file by using file name(string)
        #flow : download each cloud storage -> combine -> decryption -> save complete file -> flush tmp dir

        #download each cloud storage
        #download from s3
        combiner = file_mng(self.tmp_dir)
        tmp_dir = combiner.tmp_dir
        print "download to s3"
        self.s3_key.get_contents_to_filename(tmp_dir+"tmp1")
        print "download to ssg"
        self.ssg_key.get_contents_to_filename(tmp_dir+"tmp2")

        #combine files
        enc_buf = combiner.combine_tmp_files()
        #decryption(save complete file)
        dec = Encryption(self.tree.connection._cre.meta_pw)

        #decrpytion(filename)
        dec_buf = dec.decrypt(enc_buf)

        #flush tmp dir
        combiner.flush_tmp_dir()

        #error시엔 에러 메시지 출력 후 finally로 무조건 tmp dir 날리기
        return dec_buf

    def get_contents_to_filename(self, filename):

        dec_buf = self.get_contents_to_buf()

        with open(filename, 'wb') as f:
            f.write(dec_buf)
        print "download complete"

    def set_contents_from_file(self, fp, headers=None, replace=True, cb=None, num_cb=10,
                               policy=None, md5=None, reduced_redundancy=False, encrypt_key=False):

        self.ssg_key = self.tree.ssg_bucket.new_key(self.name)
        enc_file_path = self.tmp_dir + 'enc_file'
        #upload file by using file name(string)
        #flow : encrypt file -> split file -> upload each cloud -> flush tmp dir
        #encrypt file
        enc = Encryption(self.tree.connection._cre.meta_pw)
        enc_buf = enc.encrypt(fp.read())
        with open(enc_file_path, 'wb') as f:
            f.write(enc_buf)

        #split file
        splitter = file_mng(self.tmp_dir)
        s3_tmp, ssg_tmp = splitter.split(enc_file_path)

        #upload request
        print "upload request to api server"
        self.ssg_key.set_contents_from_filename(ssg_tmp, path.getsize(s3_tmp))
        real_name = self.ssg_key.real_name
        self.s3_key = self.tree.s3_bucket.new_key(real_name)

        # if self.s3_key.exists(real_name):
        #     raise ValueError("Key already exists. Input another Key.")

        #upload to each cloud
        #upload to s3
        print "upload to S3"
        self.s3_key.set_contents_from_filename(s3_tmp, headers, replace, cb,
                                               num_cb, policy, md5, reduced_redundancy, encrypt_key)
        #upload to ssg
        #exception 필요
        print "upload to ssg"
        self.ssg_key.send_file()
        #flush tmp dir
        splitter.flush_tmp_dir()

        #error시엔 둘다 지우는거로......
        print "upload success!"

    def set_contents_from_filename(self, filename, headers=None, replace=True, cb=None,
                                   num_cb=10, policy=None, md5=None, reduced_redundancy=False,
                                   encrypt_key=False):
        with open(filename, 'rb') as f:
            self.set_contents_from_file(f)

    def close(self):
        #close s3_key
        self.s3_key.close()
        #close ssg_key

    def exists(self):
        return self.ssg_key.exists()

    @property
    def tmp_dir(self):
        #make tmp dir location : ./tmp/
        self._tmp_dir = str(path.dirname(path.abspath(__file__)) + '/tmp/')
        if not path.isdir(self._tmp_dir):
            mkdir(self._tmp_dir)
        return self._tmp_dir


class file_mng(object):

    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

    def split(self, src_path):

        print 'start spilt'

        try:
            src_f = open(src_path, 'rb')
            src_size = path.getsize(src_path)

            #calculate each file size
            s3_size = src_size/2
            ssg_size = src_size - s3_size

            s3_buf = src_f.read(s3_size)
            print "s3_buf split complete"
            ssg_buf = src_f.read(ssg_size)
            print "ssg_buf split complete"

            #get tmp files path
            s3_path = self.tmp_dir + "tmp1"
            ssg_path = self.tmp_dir + "tmp2"

            #tmp file open
            tmp_s3 = open(s3_path, "wb")
            tmp_ssg = open(ssg_path, "wb")

            #written file from each buffer
            tmp_s3.write(s3_buf)
            tmp_ssg.write(ssg_buf)

            #close all files
            src_f.close()
            tmp_s3.close()
            tmp_ssg.close()

            print "split complete\n\n"

            return s3_path, ssg_path

        except IOError, e:
            print e
            print 'There is no "%s" file' % src_path
            return -1

    def combine_tmp_files(self):
        print 'start combine'
        try:
            #open tmp files
            tmp_s3 = open(self.tmp_dir + "tmp1", "rb")
            tmp_ssg = open(self.tmp_dir + "tmp2", "rb")
            # complete = open(file_path, 'wb')

            #write to buffer from files
            s3_buf = tmp_s3.read()
            ssg_buf = tmp_ssg.read()
            com_buf = s3_buf + ssg_buf

            # #make complete file to tmp_dir
            # complete.write(com_buf)

            #close all files
            tmp_s3.close()
            tmp_ssg.close()
            # complete.close()

        except IOError, e:
            print e
            print 'There is no "%s" file % tmp_file'
            return False

        print "combining complete"
        return com_buf

    def flush_tmp_dir(self):

        if not path.isdir(self.tmp_dir):
                pass

        else:
            rmtree(self.tmp_dir)



