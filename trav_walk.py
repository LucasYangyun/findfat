#  coding:utf-8
#
#  File:trav_walk.py
#

#  利用os.walk()函数遍历指定文件夹下的文件及文件夹

import os
import os.path


def trav_walk(pathname):
    for root, dirs, files in os.walk(pathname):
        for fil in files:
            fname = os.path.abspath(os.path.join(root, fil))
            print(fname)


trav_walk('D:\PythonPro')
