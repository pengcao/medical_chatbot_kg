#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: MedicalDataProcessor.py
@time: 2019/8/15 21:15
@desc:
'''
import os,sys
import ahocorasick
from chatbot.MedicalParams import MedicalParams

class MedicalDataProcessor(object):

    path = sys.path[0]
    medical_dict_dir = os.path.dirname(path)

    @staticmethod
    def getFeatureWordList(feature_path):
        '''

        :param feature_path:
        :return:
        '''
        feature_all_path = os.path.join(MedicalDataProcessor.medical_dict_dir, feature_path)
        feature_word_list = [word.strip() for word in open(feature_all_path, encoding='utf-8') if word.strip()]
        return feature_word_list

    @staticmethod
    def loadMedicalFeatureWords():
        '''

        :return:
        '''
        disease_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.disease_path)
        department_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.department_path)
        check_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.check_path)
        drug_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.drug_path)
        food_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.food_path)
        producer_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.producer_path)
        symptom_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.symptom_path)
        deny_word_list = MedicalDataProcessor.getFeatureWordList(MedicalParams.deny_path)
        return disease_word_list,department_word_list,check_word_list,drug_word_list,food_word_list,\
               producer_word_list,symptom_word_list,deny_word_list


    @staticmethod
    def buildActree(word_list):
        '''
        构建 Trie
        :param word_list:
        :return:
        '''
        actree = ahocorasick.Automaton()
        for index, word in enumerate(word_list):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    @staticmethod
    def getWordTypeDict(disease_word_list,department_word_list,check_word_list,drug_word_list,food_word_list,
                        producer_word_list,symptom_word_list,region_words):
        '''

        :param disease_word_list:
        :param department_word_list:
        :param check_word_list:
        :param drug_word_list:
        :param food_word_list:
        :param producer_word_list:
        :param symptom_word_list:
        :param region_words:
        :return:
        '''
        word_dict = dict()
        for word in region_words:
            word_dict[word] = []
            if word in disease_word_list:
                word_dict[word].append('disease')
            if word in department_word_list:
                word_dict[word].append('department')
            if word in check_word_list:
                word_dict[word].append('check')
            if word in drug_word_list:
                word_dict[word].append('drug')
            if word in food_word_list:
                word_dict[word].append('food')
            if word in symptom_word_list:
                word_dict[word].append('symptom')
            if word in producer_word_list:
                word_dict[word].append('producer')
        return word_dict


if __name__ == '__main__':
    path = sys.path[0]
    print(os.path.dirname(path))
    print(os.path.join(os.path.dirname(path),'dict/disease.txt'))


