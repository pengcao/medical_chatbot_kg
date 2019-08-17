#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: Neo4jDbOpr.py
@time: 2019/8/14 21:24
@desc:
'''
import sys
from util.Logger import Logger
from util.Properties import Properties
from py2neo import Graph,Node

class Neo4jDbOpr(object):
    """
    Neo4j数据库对象以及相应的操作方法
    """

    """
        private variable
    """
    __logger = Logger(sys.modules['__main__'])

    def __init__(self):
        """
        Neo4j的初始化方法,里面默认从/conf/neo4j.properties中读取关于neo4j连接的基本信息
        """
        self._graph = None
        try:
            properties = Properties('/conf/neo4j.properties').getProperties()
            self._graph = Graph(
                host=properties['neo4j.host'],                   # neo4j服务地址
                http_port=int(properties['neo4j.port']),         # neo4j端口号
                user=properties['neo4j.username'],               # neo4j的用户名，默认neo4j
                password=properties['neo4j.password'])           # neo4j的密码，默认neo4j
        except Exception as ex:
            self.__logger.info("数据库连接失败,数据库名/数据库用户名/数据库密码错误")
            self.__logger.exception(ex)

    def getNeo4jGraph(self):
        '''

        :return:
        '''
        return self._graph

    def createSimpleNodes(self,nodes,label):
        '''
        创建节点
        :param nodes:
        :param label:
        :return:
        '''
        count = 0
        error_count = 0
        try:
            for node in nodes:
                node = Node(label, name=node)
                self._graph.create(node)
                count += 1
                self.__logger.info("成功创建%s的节点有：%d个!" % (label,count))
        except Exception as ex:
            error_count += 1
            self.__logger.info("在创建%s的第%d个节点的时候出错!" % (label,count))
            self.__logger.exception(ex)
        return "%s节点成功创建%d个,%d个节点创建失败" % (label,count,error_count)

    def createRelationship(self,start_node, end_node, edges, rel_type, rel_name):
        '''
        创建节点与节点之间的关系
        :param start_node:
        :param end_node:
        :param edges:
        :param rel_type:
        :param rel_name:
        :return:
        '''
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        for edge in set(set_edges):
            edge = edge.split('###')
            start_node_name = edge[0]
            end_node_name = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, start_node_name, end_node_name, rel_type, rel_name)
            try:
                self._graph.run(query)
                count += 1
            except Exception as ex:
                self.__logger.exception(ex)


if __name__ == '__main__':
    properties = Properties('/conf/neo4j.properties').getProperties()
    print(properties)