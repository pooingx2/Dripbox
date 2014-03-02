#-*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import absolute_import
import sys
from ssg.SSGClient import connection


class SSGInterface(object):
    _connection = None
    _tree = None

    def upload(self, file_path):
        fruit = self.tree.new_fruit(file_path)
        fruit.set_contents_from_filename(file_path)

    def download(self, fruit_name):
        fruit = self.tree.get_fruit(fruit_name, False)
        buf = fruit.get_contents_to_buf()

        return buf

    @property
    def connection(self):
        if self._connection is None:
            self._connection = connection.Connection("SSGarden.key")
        return self._connection

    @property
    def tree(self):
        if self._tree is None:
            self._tree = self.connection.get_tree("drip_tree", False)
        return self._tree

#upload, download, connection