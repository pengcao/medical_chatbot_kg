#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: Logger.py
@time: 2019/8/14 21:24
@desc:
'''
import logging
import sys,os
from logging.handlers import TimedRotatingFileHandler

class Logger(object):
    """
    日志类，在这里面默人了日志输出的文件
    modules : sys.modules['__main__']
    """
    def __init__(self,modules):
        # self._logger = logging.getLogger(name)
        # 通过反射获取模块名
        file = getattr(modules, '__file__', None)
        name = os.path.splitext(os.path.basename(file))[0]
        #
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        # 日志输出文件（可以开放配置文件，在配置文件中读取配置，将日志输出到相应的目录下）
        fullfilename = os.path.dirname(sys.path[0])+'/log/run.log'
        print(' === fullfilename ', fullfilename)
        # logging模块自带的三个handler之一。继承自StreamHandler。将日志信息输出到磁盘文件上。
        # 默认情况下，日志文件可以无限增大。
        # fileHandl = logging.FileHandler(fullfilename,'a',encoding='utf8')
        # 每隔12小时创建一个新的日志文件，且将日志输出到新的日志文件中
        fileHandl = TimedRotatingFileHandler(filename=fullfilename, when="H", interval=12)
        # logging.H
        # Logger的基础配置
        fileHandl.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandl.setFormatter(formatter)

        self._logger.addHandler(fileHandl)

    def info(self,message):
        """
        @summary:在该logger上以INFO级别记录一条信息
        """
        self._logger.info(message)

    def debug(self,message):
        """
        @summary:在该logger上以DEBUG级别记录一条信息
        """
        self._logger.debug(message)

    def error(self,message):
        """
        @summary:在该logger上以ERROR级别记录一条信息
        """
        self._logger.error(message)

    def warring(self,message):
        """
        @summary:在该logger上以WARRING级别记录一条信息
        """
        self._logger.warning(message)

    def exception(self,message):
        """
        @summary:在该logger上输出异常信息
        """
        self._logger.exception(message)

if __name__ == "__main__":
    # logger = Logger(sys.modules['__main__'])
    # logger.info(" this is log info")
    print(os.path.dirname(sys.path[0])+'/log/run.log')