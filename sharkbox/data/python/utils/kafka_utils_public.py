#!/usr/bin/python
# -*- coding: utf-8 -*-

import json,os,sys,requests

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
import actuator_conf

# 用于将收到的Kafka消息存入字典
def parsing_messages(message):
    dict_log={}
    dict_log['topic'] = message.topic
    dict_log['kafka_partition'] = message.partition
    dict_log['kafka_offset'] = message.offset
    dict_log['kafka_timestamp'] = message.timestamp
    dict_log['serialized_value_size'] = message.serialized_value_size
    dict_log['kafka_value'] = json.loads(message.value.decode('utf-8'))
    return dict_log

# def writerKafkaExecCenter(path,data):
#     with open(path,"a",encoding="utf-8") as f:
#         data_json = json.dumps(data,ensure_ascii=False)
#         f.write(data_json+'\n')

# 用于将执行结果写入到数据库表中
def write_mysql(di,table_name):
    # 获取数据库链接
    con = actuator_conf.get_mysql('kafka_log')
    # 拼接sql
    sql = f"""insert into {table_name} 
              values('{di.get("topic")}'
                     ,{json.dumps(di.get("kafka_value").get("table"),ensure_ascii=False)}
                     ,{di.get("kafka_partition")}
                     ,{di.get("kafka_offset")}
                     ,{di.get("kafka_timestamp")}
                     ,{di.get("serialized_value_size")}
                     ,'{json.dumps(di.get("kafka_value"),ensure_ascii=False)}'
                     ,'{di.get("exec_step")}'
                     ,{di.get("exec_code")}
                     ,'{di.get("exec_status")}'
                     ,'{di.get("exec_time")}'
                     ,now()
                     ,now()
                     ,0
                     )"""
    # 执行sql
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        pass
    finally:
        con.close()

# 用于将重新执行的结果写入到数据库
def update_mysql(di,offset,table_name,retry_count):
    # 获取数据库链接
    con = actuator_conf.get_mysql('kafka_log')
    # 拼接sql
    sql = f"""update {table_name} set exec_step='{di.get("exec_step")}'
                                     ,exec_code={di.get("exec_code")}
                                     ,modify_time=now()
                                     ,retry_count={retry_count}+1
              where kafka_offset={offset}"""
    # 执行sql
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        pass
    finally:
        con.close()


# 用于发送消息到企业微信
def sent_to_wechat(di):
    message = f'''>>>offset值:{di.get("kafka_offset")}\n>>>执行时间:{di.get("exec_time")}\n>>>报错信息：{di.get("exec_step")}'''
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=16f73bd3-260b-4091-92f3-d93e37e4fafd"
    payload = json.dumps({"msgtype": "text",
                          "text": {
                              "content":message
                          }})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)
