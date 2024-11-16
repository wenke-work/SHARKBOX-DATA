#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import requests,json
from datetime import datetime
def get_mysql(database):
    if database == 'sharkbox_merge':
        con = pymysql.connect(
             host='192.168.1.44'
            ,port=3306
            ,user='sharkbox_merge'
            ,password='test@yjyaPro@336'
            ,database='sharkbox_merge'
        )
        return con

def result_write(table_name,batch_number):
    conn = get_mysql("sharkbox_merge")
    cursor = conn.cursor()
    if table_name == "lingxing_purchase_product":
        sql = f"select count(1) as cn from {table_name} where batch_number='{batch_number}' and (data_status='N' or sent_status='N')"
    else:
        sql = f"select count(1) as cn from {table_name} where batch_number='{batch_number}' and data_status='N'"
    cursor.execute(sql)
    result = cursor.fetchall()
    modify_time = str(datetime.now())
    if result[0][0] == 0:
        sql = f"update lingxing_merge_batch_number set status='已推送',modify_time='{modify_time}' where batch_number='{batch_number}' and table_name = '{table_name}'"
        #merge_success_to_wechat(batch_number)
    else:
        sql = f"update lingxing_merge_batch_number set status='挂起',modify_time='{modify_time}' where batch_number='{batch_number}' and table_name = '{table_name}'"
        #merge_fail_to_wechat(table_name,batch_number)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def merge_success_to_wechat(batch_number):
    message = f'''>>>批次:{batch_number}-->同步成功'''
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9b713097-759d-4f7f-a771-6d09e0245ae1"
    payload = json.dumps({"msgtype": "text",
                          "text": {
                              "content": message
                          }})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)

def merge_fail_to_wechat(table_name,batch_number):
    if table_name == "lingxing_purchase_product":
        sql = f"select purchase_number from {table_name} where batch_number='{batch_number}' and data_status='N' and sent_status='N'"
    else:
        sql = f"select count(1) as cn from {table_name} where batch_number='{batch_number}' and data_status='N'"

    message = f'''>>>批次号:{batch_number}-->同步成功\n>>>事务发起方及主方法名:{di.get("main_app")}\n>>>事务创建时间:{di.get("exec_time")}\n>>>事务执行方及执行次数:{di.get("app_name")}-->{di.get("retry_count")}\n>>>执行接口链接:{di.get("app_url")}\n>>>runState状态(4:成功)：{di.get("run_state")}\n>>>接口执行信息：{di.get("result_message")}'''
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9b713097-759d-4f7f-a771-6d09e0245ae1"
    payload = json.dumps({"msgtype": "text",
                          "text": {
                              "content": message
                          }})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)