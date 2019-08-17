# medical_chatbot_kg
this is medical chatbot based medical graph

# 运行方式
1.首先安装neo4j数据库，运行run_scripts/MedicalGraphBuilder.py  构建医疗知识图谱

2.运行run_scripts/MedicalChatBot.py  可以进行聊天，运行结果如下


3.运行run_scripts/WebApp.py，将会开启web服务，http get方法调用聊天接口http://127.0.0.1:8083/medical/%E6%84%9F%E5%86%92%E6%98%AF%E4%BB%80%E4%B9%88%E7%97%87%E7%8A%B6%EF%BC%9F

# 申明
1.本项目构建以疾病为中心的医疗知识图谱，实体规模4.4万，实体关系规模30万；
2.数据来源于互联网爬取，如有冒犯之处可以联系，进行整改；
3.如有疑问可联系：deamoncao@163.com



