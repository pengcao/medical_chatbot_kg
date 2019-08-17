#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: MedicalGraph.py
@time: 2019/8/14 21:43
@desc:
'''
import json
import os
import datetime
import sys
from util.Logger import Logger
from util.Neo4jDbOpr import Neo4jDbOpr
from py2neo import Node

class MedicalGraph(object):

    """
        private variable
    """
    __logger = Logger(sys.modules['__main__'])

    def __init__(self):
        '''

        '''
        self.neo4jDbOpr = Neo4jDbOpr()
        self.neo4jGraph = self.neo4jDbOpr.getNeo4jGraph()

    def loadCorpus(self,medicalPath):
        '''

        :param medicalPath: medical corpus path
        :return: drugs, foods, checks, departments, producers, symptoms, diseases, disease_infos,rels_check,
                  rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer,
                  rels_recommanddrug,rels_symptom, rels_acompany, rels_category
                  以上返回结果的解释如下变量所示
        '''
        self.__logger.info(' ### start load medical corpus !')
        # 节点
        # 药品
        drugs = []
        # 食物
        foods = []
        # 检查
        checks = []
        # 科室
        departments = []
        # 药品大类
        producers = []
        # 疾病
        diseases = []
        # 症状
        symptoms = []

        # 疾病信息
        disease_infos = []

        # 节点之间的关系
        # 科室－科室关系
        rels_department = []
        # 疾病－忌吃食物关系
        rels_noteat = []
        # 疾病－宜吃食物关系
        rels_doeat = []
        # 疾病－推荐吃食物关系
        rels_recommandeat = []
        # 疾病－通用药品关系
        rels_commonddrug = []
        # 疾病－热门药品关系
        rels_recommanddrug = []
        # 疾病－检查关系
        rels_check = []
        # 厂商－药物关系
        rels_drug_producer = []

        # 疾病症状关系
        rels_symptom = []
        # 疾病并发关系
        rels_acompany = []
        # 疾病与科室之间的关系
        rels_category = []

        # 对medicalPath里面的数据进行解析
        for data in open(medicalPath,encoding='utf-8'):
            disease_dict = {}
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:
                     rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']

            if  'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])
                # 忌口
                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])
                # 食疗
                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check

            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease_dict)

        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos,\
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
               rels_symptom, rels_acompany, rels_category


    def createDiseasesNodes(self, disease_infos):
        '''
        创建disease information的节点
        :param disease_infos:
        :return:
        '''
        count = 0
        try:
            for disease_dict in disease_infos:
                count += 1
                node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                            prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                            easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                            cure_department=disease_dict['cure_department']
                            ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
                self.neo4jGraph.create(node)
            self.__logger.info("成功创建disease_infos的节点有：%d个!" % (count))
        except Exception as ex:
            self.__logger.info("在创建disease_infos的第%d个节点的时候出错!" % (count))
            self.__logger.exception(ex)

    def createMedicalGraphNodes(self,drugs, foods, checks, departments, producers, symptoms, disease_infos):
        '''

        :param drugs:
        :param foods:
        :param checks:
        :param departments:
        :param producers:
        :param symptoms:
        :param disease_infos:
        :return:
        '''

        self.createDiseasesNodes(disease_infos)
        drug_info = self.neo4jDbOpr.createSimpleNodes('Drug', drugs)
        self.__logger.info(drug_info)
        food_info = self.neo4jDbOpr.createSimpleNodes('Food', foods)
        self.__logger.info(food_info)
        check_info = self.neo4jDbOpr.createSimpleNodes('Check', checks)
        self.__logger.info(check_info)
        department_info = self.neo4jDbOpr.createSimpleNodes('Department', departments)
        self.__logger.info(department_info)
        producer_info = self.neo4jDbOpr.createSimpleNodes('producer', producers)
        self.__logger.info(producer_info)
        symptom_info = self.neo4jDbOpr.createSimpleNodes('Symptom', symptoms)
        self.__logger.info(symptom_info)

    def createMedicalGraphRels(self,rels_check, rels_recommandeat,rels_noteat, rels_doeat, rels_department, rels_commonddrug,
                         rels_drug_producer, rels_recommanddrug,rels_symptom,rels_acompany, rels_category):
        '''

        :param rels_check:
        :param rels_recommandeat:
        :param rels_noteat:
        :param rels_doeat:
        :param rels_department:
        :param rels_commonddrug:
        :param rels_drug_producer:
        :param rels_recommanddrug:
        :param rels_symptom:
        :param rels_acompany:
        :param rels_category:
        :return:
        '''

        self.neo4jDbOpr.createRelationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.neo4jDbOpr.createRelationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.neo4jDbOpr.createRelationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.neo4jDbOpr.createRelationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.neo4jDbOpr.createRelationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.neo4jDbOpr.createRelationship('producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.neo4jDbOpr.createRelationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.neo4jDbOpr.createRelationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.neo4jDbOpr.createRelationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.neo4jDbOpr.createRelationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.neo4jDbOpr.createRelationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')




    def creatMedicalGraph(self,medicalPath):
        '''

        :param medicalPath:
        :return:
        '''
        drugs, foods, checks, departments, producers, symptoms, diseases, disease_infos,rels_check, rels_recommandeat,\
        rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom,\
        rels_acompany, rels_category = self.loadCorpus(medicalPath)
        # 创建基础节点
        self.createMedicalGraphNodes(drugs, foods, checks, departments, producers, symptoms, disease_infos)
        # 创建节点之间的关系
        self.createMedicalGraphRels(rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department,
                                    rels_commonddrug,rels_drug_producer, rels_recommanddrug, rels_symptom,
                                    rels_acompany, rels_category)


if __name__ == '__main__':
    medicalGraph = MedicalGraph()
    medicalGraph.creatMedicalGraph()
