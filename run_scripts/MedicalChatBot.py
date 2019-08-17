#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: MedicalChatBot.py
@time: 2019/8/17 18:47
@desc:
'''
from chatbot.MedicalChatbot import MedicalChatbot
from util.Neo4jDbOpr import Neo4jDbOpr


if __name__ == '__main__':
    medicalChatbot = MedicalChatbot()
    neo4jDbOpr = Neo4jDbOpr()
    neo4jGraph = neo4jDbOpr.getNeo4jGraph()
    while 1:
        question = input('用户:')
        answer = medicalChatbot.getQuestionAnwser(question,neo4jGraph)
        print('小智:', answer)