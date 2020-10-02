#-*- coding:utf-8 -*-
import os

path = Workpath = os.path.dirname(os.path.abspath(__file__))
# 工程根目录

if os.name == 'nt':
    Workpath = path.split('\\')
else:
    Workpath = path.split('/')
# 工作目录分割

next_ = None
if os.name == 'nt':
    next_ = '\\'
else:
    next_ = '/'
# 针对 Linux 和 windows 的不同，更改路径中的 反斜杠(\) 或 斜杠(/)

def dir_mix(*dirs):
    return next_.join(dirs)
# 路径拼合函数

def path_read(path):
    return next_.join(path)
# 读取path数据，合成子路径

root = path_read(Workpath[:-1])

Package_path = path_read([root,"Package"]) # Package 扫描目录
