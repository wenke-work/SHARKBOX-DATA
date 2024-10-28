#!/usr/bin/python

import requests
import json,os,sys

parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_directory + '/conf')
sys.path.append(parent_directory + '/utils')
import table_columns
import actuator_conf
import login

spark_name="test"

def getUserWarehouseList(session):
    url = "http://192.168.1.42:81/meio/User/GetUserWarehouseList"
    payload={}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }
    response = session.get(url, headers=headers, data=payload)
    list_user = response.json()
    data_list = list_user.get("data")
    spark = actuator_conf.getSpark(spark_name)
    schema = table_columns.tableColumn("GetUserWarehouseList")
    ret_df = spark.createDataFrame(data_list,schema)
    ret_df.createOrReplaceTempView("temp")
    spark.sql("insert overwrite table test.get_user_warehouse_list select * from temp")

if __name__=="__main__":
    session = requests.session()                   #获取一个session
    status_code = login.loginToWMS(session)        #登录
    if status_code == "登录成功":
        getUserWarehouseList(session)              #调用接口获取数据
    else:
        print(status_code)
