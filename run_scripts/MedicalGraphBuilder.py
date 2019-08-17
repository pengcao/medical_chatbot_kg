#!/usr/bin/env python
# encoding: utf-8
'''
@author: caopeng
@license: (C) Copyright 2016-2020, Big Bird Corporation Limited.
@contact: deamoncao100@gmail.com
@software: garner
@file: MedicalGraphBuilder.py
@time: 2019/8/17 15:42
@desc:
'''
from knowledge_grap.MedicalGraph import MedicalGraph
import datetime

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    medicalGraph = MedicalGraph()
    medicalGraph.creatMedicalGraph()
    endtime = datetime.datetime.now()
    print(' === starttime : ',str(starttime))
    print(' ===   endtime : ', str(endtime))