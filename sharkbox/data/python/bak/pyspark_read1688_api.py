#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, json, time, sys
import requests
parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_directory + '/conf')
sys.path.append(parent_directory + '/utils')
import pyspark_utils_public
import actuator_conf
import table_columns

num = 0
app_key = '9007550'
url = "https://gw.open.1688.com/openapi/param2/1/com.alibaba.product/alibaba.category.get/{}".format(app_key)
writerPath = "C:\\Users\\Administrator\\Desktop\\files\\temp\\tmp\\test_log.txt"
global_list = []
def callApi(id):
    global num
    global global_list
    params = {
        "categoryID": id
    }
    paraStr = pyspark_utils_public.paramHandle1688(params)
    index_start = url.find("openapi/")
    signatureStr = url[index_start+8:]+paraStr
    signature = pyspark_utils_public.encryption1688(signatureStr)
    params['_aop_signature'] = signature
    num += 1
    print(num)
    response = requests.post(url,data=params)
    reuList = response.json().get("categoryInfo")[0].get("childCategorys")
    for product in reuList:
        product['super_id'] = id
        global_list.append(product)
        if product['isLeaf'] == False:
            callApi(product['id'])


def execPyspark():
    spark = actuator_conf.getSpark("insert_ods_1688_ods_product_category")
    schema = table_columns.tableColumn("insert_ods_1688_ods_product_category")
    ret_df = spark.createDataFrame(global_list,schema)
    ret_df.createOrReplaceTempView("temp")
    spark.sql("insert overwrite table ods_1688.ods_product_category select * from temp")


if __name__=="__main__":
    callApi(0)
    execPyspark()
