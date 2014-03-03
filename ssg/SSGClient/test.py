#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import path

from ssg.SSGClient.connection import Connection


if __name__ == "__main__":
    current_dir = path.dirname(path.abspath(__file__))
    conn = Connection(current_dir + '/../../SSGarden.key')
    print conn.ssg_conn.header
    tree_name = 'upload_test'
    #tree_name = 'test_tree'
    fruit_name = 'test1'
    target_file = current_dir + '/test.png'
    des_file = current_dir + '/되어랏.png'

    test_tree = conn.get_tree(tree_name, False)
    # print test_tree.s3_bucket.name
    fruit = test_tree.get_fruit(fruit_name)#, False)
    # print fruit.exists()
    # print "ttt" + str(fruit.get_metadata())
    # fruit.get_contents_to_filename(des_file)
    # fruit.get_contents_to_filename(target_file)
    with open(target_file, 'rb') as f:
        fruit.set_contents_from_file(f)
    # print fruit.s3_key.name



    # fruit.set_contents_from_filename(target_file)
    # print test_tree.get_location()
    # for f in fruit_list:
    #     print f.__dict__
    # conn.create_basket('7')
    # #conn = Connection('/home/sungjin/SSGarden.key')
    #
    # tree = conn.get_tree(tree_name)
    # print 'tree : ' + tree.name
    # fruit = tree.get_fruit(fruit_name)
    #
    # print 'fruit : ' + fruit.name

    # test_tree = conn.create_Tree(tree_name)

    # fruit.get_contents_to_filename(des_file)
    # fruit.set_contents_from_filename('dd')
    # error print tree.get_location()

    #
    # fruit = basket.get_fruit("test2")
    #
    # #fruit.set_contents_from_filename(current_dir + '/testpic.png')
    # #fruit.set_contents_from_filename(current_dir + '/testfile.txt')
    # #fruit.set_contents_from_filename(current_dir + '/testfile.txt')
    # #fruit.set_contents_from_filename(current_dir + '/testdoc.doc')
    #
    # fruit.get_contents_to_filename('test')
