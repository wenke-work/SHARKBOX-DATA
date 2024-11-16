#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
功能 :加工计划_采购-单品明细数据处理, 对应数据库lingxing_purchase_processing_plan表
"""
import sys,os,json
import requests
from datetime import datetime
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
import public_utils

#host='106.53.113.34:8081'
host='192.168.1.48:8081'

def none_to_string(value):
    return "" if value is None else str(value)


def call_api(para):
    url = "http://%s/openApi/process/saveAction" % (host)
    payload = json.dumps(para)
    headers = {
        'Content-Type': 'application/json',
        'tenant':'HZ007'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=(10,10))
        print(response.json())
        return response.json()
    except requests.exceptions.Timeout as e:
        return {'code': '-1', 'msg': 'requests.exceptions.Timeout: 请求超时'}
    except Exception as e:
        return {'code': '1','msg': '调用接口时程序报错'}

def call_proc(conn):
    cursor = conn.cursor()
    cursor.callproc('proc_lingxing_purchase_processing_plan')
    cursor.close()

def one_sub_item(conn,batch_number):
    exec_data = []
    cursor = conn.cursor()
    sql = f'''select combination_product_name,combination_sku,processing_plan_number,purchase_number,planned_processing_volume,combination_ratio,product_name,sku,warehouse
              from lingxing_purchase_processing_plan where ifnull(data_status,"")<>"Y" and data_number=1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    sub_product_list = []
    for combination_product_name,combination_sku,processing_plan_number,purchase_number,planned_processing_volume,combination_ratio,product_name,sku,warehouse in result:
        sub_product_dit ={
                "purchaseNo": none_to_string(purchase_number),
                "subAmount": none_to_string(planned_processing_volume),
                "subNumber": none_to_string(combination_ratio),
                "subProductName": none_to_string(product_name),
                "subSku": none_to_string(sku)
            }
        sub_product_list.append(sub_product_dit)
        para_data = {
                "mainProductName": none_to_string(combination_product_name),
                "mainSku": none_to_string(combination_sku),
                "processPlanNo": none_to_string(processing_plan_number),
                "warehouse": none_to_string(warehouse),
                "subProductList": sub_product_list
            }
        response = call_api(para_data)
        modify_time = str(datetime.now())
        if response.get("code") == '201':
            exec_data.append((processing_plan_number,'Y',modify_time,response))
        else:
            exec_data.append((processing_plan_number,'N',modify_time,response))
    for exec in exec_data:
        exec_log = json.dumps(exec[3], ensure_ascii=False)
        sql = f"""update lingxing_purchase_processing_plan set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where processing_plan_number='{exec[0]}'"""
        cursor.execute(sql)
        conn.commit()
    cursor.close()

def many_sub_item(conn,batch_number):
    cursor = conn.cursor()
    sql = f'''select distinct processing_plan_number as processing_plan_number from lingxing_purchase_processing_plan where data_status<>"Y" and data_number>1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    for resu in result:
        processing_plan_number = resu[0]
        sql = f'''select combination_product_name,combination_sku,processing_plan_number,purchase_number,planned_processing_volume,combination_ratio,product_name,sku,warehouse
                from lingxing_purchase_processing_plan where data_status<>"Y" and processing_plan_number="{processing_plan_number}" and batch_number="{batch_number}"'''
        cursor.execute(sql)
        result_many = cursor.fetchall()
        sub_list = []
        modify_time = str(datetime.now())
        num = 0
        for combination_product_name,combination_sku,processing_plan_number,purchase_number,planned_processing_volume,combination_ratio,product_name,sku,warehouse in result_many:
            sub_product_dit = {
                "purchaseNo": none_to_string(purchase_number),
                "subAmount": none_to_string(planned_processing_volume),
                "subNumber": none_to_string(combination_ratio),
                "subProductName": none_to_string(product_name),
                "subSku": none_to_string(sku)
            }
            sub_list.append(sub_product_dit)
            num = num + 1
            if len(result_many) == num:
                para_data = {
                    "mainProductName": none_to_string(combination_product_name),
                    "mainSku": none_to_string(combination_sku),
                    "processPlanNo": none_to_string(processing_plan_number),
                    "warehouse": none_to_string(warehouse),
                    "subProductList": sub_list
                }
                response = call_api(para_data)
                if response.get("code") == '201':
                    exec = [processing_plan_number, 'Y', modify_time,response]
                else:
                    exec = [processing_plan_number,'N',modify_time,response]
                exec_log = json.dumps(exec[3], ensure_ascii=False)
                sql = f"""update lingxing_purchase_processing_plan set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where processing_plan_number='{exec[0]}'"""
                cursor.execute(sql)
                conn.commit()
    cursor.close()

def lingxing_data_processing(batch_number):
    conn = public_utils.get_mysql('sharkbox_merge')
    call_proc(conn)
    one_sub_item(conn,batch_number)
    many_sub_item(conn,batch_number)
    public_utils.result_write("lingxing_purchase_processing_plan", batch_number)
    conn.close()


#lingxing_data_processing('e7ec55de-ba34-4ad8-8723-a18facb38f87')