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
                             , bootstrap_servers=['192.168.1.44:1541', '192.168.1.44:1542', '192.168.1.44:1543']
                             , auto_offset_reset='latest'
                             , group_id=group_name
                             , max_poll_records=1
                             )
    return consumer


# MySQL执行配置
def get_mysql(database):
    if database == 'kafka_log':
        con = pymysql.connect(
             host='192.168.1.44'
            ,port=3306
            ,user='root'
            ,password='lzhl@888'
            ,database='kafka_log'
        )
        return con
    elif database == 'sharkbox_transaction':
        con = pymysql.connect(
             host='192.168.1.44'
            ,port=3306
            ,user='sharkbox_transaction'
            ,password='sharkbox@888'
            ,database='sharkbox_transaction'
        )
        return con
