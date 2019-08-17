#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: QuestionClassifier.py
@time: 2019/8/15 21:58
@desc:
'''
from chatbot.MedicalParams import MedicalParams
from chatbot.MedicalDataProcessor import MedicalDataProcessor

class QuestionClassifier(object):

    def __init__(self):
        # 加载特征词
        disease_word_list, department_word_list, check_word_list, drug_word_list, food_word_list, \
        producer_word_list, symptom_word_list, deny_word_list = MedicalDataProcessor.loadMedicalFeatureWords()
        self.deny_words = deny_word_list
        # 构建
        self.region_words = set(department_word_list + disease_word_list + check_word_list + drug_word_list +
                                food_word_list + producer_word_list + symptom_word_list)

        # 构造领域actree
        self.region_tree = MedicalDataProcessor.buildActree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = MedicalDataProcessor.getWordTypeDict(disease_word_list,department_word_list,check_word_list,drug_word_list,food_word_list,
                        producer_word_list,symptom_word_list,self.region_words)


    def classifyQquestion(self, question):
        '''
        问题分类
        :param question:
        :return:
        '''
        data = {}
        medical_dict = self.getQuestionMedicalDict(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        if self.checkQuestion(MedicalParams.symptom_question_words, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.checkQuestion(MedicalParams.symptom_question_words, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.checkQuestion(MedicalParams.cause_question_words, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.checkQuestion(MedicalParams.acompany_question_words, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.checkQuestion(MedicalParams.food_question_words, question) and 'disease' in types:
            deny_status = self.checkQuestion(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        #已知食物找疾病
        if self.checkQuestion(MedicalParams.food_question_words+MedicalParams.cure_question_words, question) and 'food'\
                in types:
            deny_status = self.checkQuestion(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品
        if self.checkQuestion(MedicalParams.drug_question_words, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.checkQuestion(MedicalParams.cure_question_words, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.checkQuestion(MedicalParams.check_question_words, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.checkQuestion(MedicalParams.check_question_words+MedicalParams.cure_question_words, question) and \
                'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        #　症状防御
        if self.checkQuestion(MedicalParams.prevent_question_words, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)

        # 疾病医疗周期
        if self.checkQuestion(MedicalParams.lasttime_question_words, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.checkQuestion(MedicalParams.cureway_question_words, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.checkQuestion(MedicalParams.cureprob_question_words, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # 疾病易感染人群
        if self.checkQuestion(MedicalParams.easyget_question_words, question) and 'disease' in types :
            question_type = 'disease_easyget'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


    def getQuestionMedicalDict(self, question):
        '''
        问句过滤
        :param question:
        :return:
        '''
        region_word_list = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_word_list.append(wd)
        stop_word_list = []
        for wd1 in region_word_list:
            for wd2 in region_word_list:
                if wd1 in wd2 and wd1 != wd2:
                    stop_word_list.append(wd1)
        final_word_list = [word for word in region_word_list if word not in stop_word_list]
        final_dict = {word:self.wdtype_dict.get(word) for word in final_word_list}

        return final_dict


    def checkQuestion(self, word_list, question):
        '''
        提问特征词分类
        :param word_list:
        :param question:
        :return:
        '''
        for word in word_list:
            if word in question:
                return True
        return False



