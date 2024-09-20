#!/usr/bin/python

from pyspark.sql import SparkSession
from kafka import KafkaConsumer
import pymysql


# spark执行配置
def get_spark(name):
    spark = SparkSession.builder \
        .appName(name) \
        .enableHiveSupport() \
        .getOrCreate()
    return spark


# kafka执行配置
def get_consumer(topic_name,group_name):
    consumer = KafkaConsumer(topic_name
                             , bootstrap_servers=['node-1:9092', 'node-2:9092', 'node-3:9092']
                             , auto_offset_reset='latest'
                             , group_id=group_name
                             , max_poll_records=1
                             )
    return consumer


# MySQL执行配置
def get_mysql(database):
    if database == 'kafka_log':
        con = pymysql.connect(
             host='172.16.0.9'
            ,port=3306
            ,user='kafka_log'
            ,password='sharkbox@kaWkjyPro@336'
            ,database='kafka_log'
        )
        return con
    elif database == 'sharkbox_transaction':
        con = pymysql.connect(
             host='172.16.0.9'
            ,port=3306
            ,user='sharkbox_transaction'
            ,password='sharkbox@pro@888'
            ,database='sharkbox_transaction'
        )
        return con