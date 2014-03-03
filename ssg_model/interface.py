#-*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import
from urllib2 import quote
from ssg.SSGClient import connection
from os import path


class SSGInterface(object):
    _connection = None
    _tree = None

    def upload(self, user, file_path, fp):
        upload_path = user + ' / ' + file_path

        fruit = self.tree.new_fruit(quote(upload_path))
        fruit.set_contents_from_file(fp=fp)

    def download(self, fruit_name):
        print fruit_name
        fruit = self.tree.get_fruit(quote(fruit_name), False)
        buf = fruit.get_contents_to_buf()

        return buf

    @property
    def connection(self):
        if self._connection is None:
            dir = path.dirname(path.abspath(__file__))
            self._connection = connection.Connection(dir+"/SSGarden.key")
        return self._connection

    @property
    def tree(self):
        if self._tree is None:
            self._tree = self.connection.get_tree("drip_tree", False)
        return self._tree

#upload, download, connection