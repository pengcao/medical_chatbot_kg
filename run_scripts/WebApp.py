#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: WebApp.py
@time: 2019/8/16 10:00
@desc:
'''
import sys
from util.Logger import Logger
from flask import Flask,jsonify
from flask_restful import  Api, Resource
from util.Neo4jDbOpr import Neo4jDbOpr
from chatbot.MedicalChatbot import MedicalChatbot

app = Flask(__name__)
api = Api(app)

medicalChatbot = MedicalChatbot()
neo4jDbOpr = Neo4jDbOpr()
neo4jGraph = neo4jDbOpr.getNeo4jGraph()

__logger = Logger(sys.modules['__main__'])

class MedicalCahtApi(Resource):
    def get(self, question):
        try:
            answer = medicalChatbot.getQuestionAnwser(question, neo4jGraph)
            return jsonify({'code': '200','question':question,'message':'成功!','result':answer})
        except Exception as ex:
            self.__logger.exception(ex)
            return jsonify({'code': '404','question':question,'message':'失败!','result':'服务出错!'})


# 设置路由
api.add_resource(MedicalCahtApi, '/medical/<question>')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8083, debug=True)
