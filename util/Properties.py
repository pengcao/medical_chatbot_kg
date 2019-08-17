#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: Properties.py
@time: 2019/8/14 21:25
@desc:
'''
import sys,os
import re
import codecs
import tempfile
from util.Logger import Logger

class Properties(object):
    """
        private variable
    """
    __logger = Logger(sys.modules['__main__'])

    def __init__(self,fileName):
        path = sys.path[0]
        self.filePath = os.path.dirname(path) + fileName
        # self.file_name = self.filePath
        self.properties = {} # 关于配置信息的字典对象
        self.properties = self.initProperties()


    def initProperties(self):
        '''
        初始化配置文件，将配置文件转换成字典对象并且返回
        :return:  字典结构的配置文件
        '''
        try:
            pro_file = open(self.filePath,"Ur")
            for line in pro_file.readlines():
                line = line.strip().replace('\n','')
                if line.find("#")!= -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0])+1:]
                    self.properties[strs[0].strip()] = strs[1].strip()
            try:
                pro_file.close()
            except Exception as ex:
                self.__logger.error("关闭配置文件时，出现错误")
        except Exception as ex:
            raise self.__logger.error("读取配置文件时，出现错误")
        return self.properties

    def getProperties(self):
        '''
        获取配置文件的信息
        :return:
        '''
        return self.properties

    def get(self,key):
        '''
        根据key获取配置文件中的value
        :param key:
        :return:
        '''
        if self.properties.__contains__(key):
            return self.properties[key]
        else:
            return None

    def replaceProperty(self, filePath, orignStr, newStr):
        '''
        修改配置文件的内容
        :param filePath:
        :param orignStr:
        :param newStr:
        :return:
        '''
        # 创建临时文件
        tmpFile = tempfile.TemporaryFile()
        #
        if os.path.exists(filePath):
            # 读取原始文件
            orignOpenObj = codecs.open(filePath, 'r', encoding='utf8')
            # 匹配模式
            pattern = re.compile(r'' + orignStr)
            # 替换文本在文件中是否存在  标识器
            found = None
            # 读取原文件
            for line in orignOpenObj:
                # 判断替换文本是否存在 且没有被注释
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    # 找到的话，就替换
                    line = re.sub(orignStr, newStr, line)
                # 写入临时文件
                tmpFile.write(line.encode('utf-8'))
            # 追加新的配置属性信息
            if not found:
                tmpFile.write(('\n' + newStr).encode('utf-8'))
            #
            orignOpenObj.close()
            tmpFile.seek(0)
            # 读取临时文件中的所有内容
            content = tmpFile.read()
            # 判断文件是否存在
            if os.path.exists(filePath):
                os.remove(filePath)
            # 将临时文件中的内容写入原文件
            orignWriteObj = codecs.open(filePath, 'w', encoding='utf8')
            orignWriteObj.write(content.decode('utf-8'))
            orignWriteObj.close()
            # 关闭临时文件，同时也会自动删掉临时文件
            tmpFile.close()
        else:
            print("file %s not found" % filePath)

    def put(self, key, value):
        '''
        修改配置文件的内容
        :param key:
        :param value:
        :return:
        '''
        self.properties[key] = value
        self.replaceProperty(self.filePath, key + '=.*', key + '=' + value)

    def putOneAndSaveNewFile(self,key,value,newFilePath):
        '''
        更改配置文件中的某一个属性的值
        :param key:
        :param value:
        :param newFilePath:
        :return:
        '''
        #
        orignStr=key + '=.*'
        newStr=key + '=' + value
        # 创建临时文件
        newFile=codecs.open(newFilePath, 'w', encoding='utf8')
        #
        if os.path.exists(self.filePath):
            # 读取原始文件
            orignOpenObj = codecs.open(self.filePath, 'r', encoding='utf8')
            # 匹配模式
            pattern = re.compile(r'' + orignStr)
            # 替换文本在文件中是否存在  标识器
            found = None
            # 读取原文件
            for line in orignOpenObj:
                # 判断替换文本是否存在 且没有被注释
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    # 找到的话，就替换
                    line = re.sub(orignStr, newStr, line)
                # 写入临时文件
                newFile.write(line)
            # 追加新的配置属性信息
            if not found:
                newFile.write('\n' + newStr)
            #
            orignOpenObj.close()
            newFile.close()

    def putMulitAndSaveNewFile(self,newDictObj,newFilePath):
        '''
        更改配置文件中的多个属性的值
        :param newDictObj:
        :param newFilePath:
        :return:
        '''
        # 创建新的文件
        newFile=codecs.open(newFilePath, 'w', encoding='utf8')
        #
        if os.path.exists(self.filePath):
            # 读取原始文件
            orignOpenObj = codecs.open(self.filePath, 'r', encoding='utf8')
            # 匹配模式
            # pattern = re.compile(r'' + orignStr)
            # 替换文本在文件中是否存在  标识器
            # found = None
            #
            regTrueKey=[]
            # 读取原文件
            for line in orignOpenObj:
                # 判断替换文本是否存在 且没有被注释
                for key in newDictObj.keys():
                    orignStr = key + '=.*'
                    newStr = key + '=' + newDictObj[key]
                    pattern = re.compile(r'' + orignStr)
                    if pattern.search(line) and not line.strip().startswith('#'):
                        regTrueKey.append(key)
                        # 找到的话，就替换
                        line = re.sub(orignStr, newStr, line)
                        break
                # 写入临时文件
                newFile.write(line)
            # 去除掉已经匹配上的
            for key in regTrueKey:
                if key in newDictObj.keys():
                    del newDictObj[key]
            # 没有匹配的，即为新增加的内容，将新增的内容写进到配置文件中
            if newDictObj.__len__() > 0:
                for key in newDictObj.keys():
                    newStr = key + '=' + newDictObj[key]
                    newFile.write('\n' + newStr)
            orignOpenObj.close()
            newFile.close()

if __name__ == '__main__':
    print()
    dict = {"h1":1,"h2":2}
    print(dict.__contains__("h1"))
    filename = '/conf/email.properties'
    properties = Properties(filename)
    # properties.put('others23','123456')
    newFilepath='C:/01.develop/code/self/bh.toolkit.data.basic/conf/email_new.properties'
    newDict={}
    newDict['country']='china'
    newDict['province']='GuangDong'
    newDict['city']='ShenZhen'
    newDict['sender']='caopeng557@pingan.com.cn'
    newDict['others23']='pingan-net'
    properties.putMulitAndSaveNewFile(newDict,newFilepath)
    # receiverListStr = properties.getValStrByKey("receiver")
    # print("receiver : ",receiverListStr)
    # list = receiverListStr.split(";")
    # print("  list : ",list)
