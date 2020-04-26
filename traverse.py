#  coding:utf-8
#
#  File:traverse.py

#  利用递归算法输出指定目录下的所有文件及文件夹

import os


def traverse(pathname):
    for item in os.listdir(pathname):
        fullitem = os.path.join(pathname, item)
        print(fullitem)
        if os.path.isdir(fullitem):
            traverse(fullitem)


traverse('D:/PythonPro')
