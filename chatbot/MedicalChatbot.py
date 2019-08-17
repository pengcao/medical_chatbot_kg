#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: MedicalChatbot.py
@time: 2019/8/15 22:40
@desc:
'''
from chatbot.QuestionClassifier import QuestionClassifier
from chatbot.AnswerEngine import AnswerEngine
from chatbot.QuestionParser import QuestionParser
from util.Neo4jDbOpr import Neo4jDbOpr

class MedicalChatbot(object):

    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.engine = AnswerEngine()

    def getQuestionAnwser(self, question,neo4jGraph):
        answer = '您好，我是小智医药智能助理，希望可以帮到您。如果没答上来，可到http://jib.xywy.com/上搜索，' \
                 '或者联系我们。祝您身体棒棒！'
        res_classify = self.classifier.classifyQquestion(question)
        if not res_classify:
            return answer
        res_sql = self.parser.getAllQuestionSql(res_classify)
        final_answers = self.engine.getAnswer(res_sql,neo4jGraph)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    medicalChatbot = MedicalChatbot()
    neo4jDbOpr = Neo4jDbOpr()
    neo4jGraph = neo4jDbOpr.getNeo4jGraph()
    while 1:
        question = input('用户:')
        answer = medicalChatbot.getQuestionAnwser(question,neo4jGraph)
        print('小智:', answer)


