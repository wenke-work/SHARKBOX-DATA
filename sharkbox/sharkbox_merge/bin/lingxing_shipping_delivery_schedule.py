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
    url = "http://%s/openApi/outbound/saveAction" % (host)
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
    cursor.callproc('proc_lingxing_shipping_delivery_schedule')
    cursor.close()

def one_sub_item(conn,batch_number):
    exec_data = []
    cursor = conn.cursor()
    sql = f'''select batch_remarks,fnsku,plan_number,product_name,notes,sku,delivery_warehouse,planned_shipment_quantity,create_batch_number
              from lingxing_shipping_delivery_schedule where ifnull(data_status,"")<>"Y" and data_number=1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    sub_product_list = []
    for batch_remarks,fnsku,plan_number,product_name,notes,sku,delivery_warehouse,planned_shipment_quantity,create_batch_number in result:
        para = {
              "fnsku": none_to_string(fnsku),
              "planNo": none_to_string(plan_number),
              "productName": none_to_string(product_name),
              "quantity": none_to_string(planned_shipment_quantity),
              "remark": none_to_string(notes),
              "sku": none_to_string(sku),
              "warehouseName": none_to_string(delivery_warehouse)
            }
        sub_product_list.append(para)
        para_data = {
            "batchNo": none_to_string(create_batch_number),
            "batchRemark": none_to_string(batch_remarks),
            "delList": sub_product_list
        }
        response = call_api(para_data)
        modify_time = str(datetime.now())
        if response.get("code") == '201':
            exec_data.append((plan_number,'Y',modify_time,response))
        else:
            exec_data.append((plan_number,'N',modify_time,response))
    for exec in exec_data:
        exec_log = json.dumps(exec[3], ensure_ascii=False)
        sql = f"""update lingxing_shipping_delivery_schedule set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where create_batch_number='{exec[0]}'"""
        cursor.execute(sql)
        conn.commit()
    cursor.close()

def many_sub_item(conn,batch_number):
    cursor = conn.cursor()
    sql = f'''select distinct create_batch_number as create_batch_number from lingxing_shipping_delivery_schedule where ifnull(data_status,"")<>"Y" and data_number>1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    for resu in result:
        create_batch_number = resu[0]
        sql = f'''select batch_remarks,fnsku,plan_number,product_name,notes,sku,delivery_warehouse,planned_shipment_quantity,create_batch_number
                from lingxing_shipping_delivery_schedule where ifnull(data_status,"")<>"Y" and create_batch_number="{create_batch_number}" and batch_number="{batch_number}"'''
        cursor.execute(sql)
        result_many = cursor.fetchall()
        sub_list = []
        modify_time = str(datetime.now())
        num = 0
        for batch_remarks,fnsku,plan_number,product_name,notes,sku,delivery_warehouse,planned_shipment_quantity,create_batch_number in result_many:
            sub_product_dit = {
                "fnsku": none_to_string(fnsku),
                "planNo": none_to_string(plan_number),
                "productName": none_to_string(product_name),
                "quantity": none_to_string(planned_shipment_quantity),
                "remark": none_to_string(notes),
                "sku": none_to_string(sku),
                "warehouseName": none_to_string(delivery_warehouse)
            }
            sub_list.append(sub_product_dit)
            num = num + 1
            if len(result_many) == num:
                para_data = {
                    "batchNo": none_to_string(create_batch_number),
                    "batchRemark": none_to_string(batch_remarks),
                    "delList": sub_list
                }
                response = call_api(para_data)
                if response.get("code") == '201':
                    exec = [create_batch_number, 'Y', modify_time,response]
                else:
                    exec = [create_batch_number,'N',modify_time,response]
                exec_log = json.dumps(exec[3], ensure_ascii=False)
                sql = f"""update lingxing_shipping_delivery_schedule set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where create_batch_number='{exec[0]}'"""
                cursor.execute(sql)
                conn.commit()
    cursor.close()

def lingxing_data_processing(batch_number):
    conn = public_utils.get_mysql('sharkbox_merge')
    call_proc(conn)
    one_sub_item(conn,batch_number)
    many_sub_item(conn,batch_number)
    public_utils.result_write("lingxing_shipping_delivery_schedule", batch_number)
    conn.close()


#lingxing_data_processing('e7ec55de-ba34-4ad8-8723-a18facb38f87')