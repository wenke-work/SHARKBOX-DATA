#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
功能 :供应商档案_供应商数据处理, 对应数据库lingxing_supplier表
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

def add_shipping_order(para):
    url = "http://%s/openApi/purchase/saveDeliveryData" % (host)
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

def one_sub_item(conn,batch_number):
    exec_data = []
    cursor = conn.cursor()
    sql = f'''select purchase_number,logistics_provider,logistics_tracking_number
              from lingxing_purchase_product where IFNULL(sent_status,"")<>"Y" and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    for purchase_number,logistics_provider,logistics_tracking_number in result:
        add_shipping = {
            "deliveryCompany": none_to_string(logistics_provider),
            "deliveryNo": none_to_string(logistics_tracking_number),
            "purchaseNo": none_to_string(purchase_number)
        }
        response_order = add_shipping_order(add_shipping)
        modify_time = str(datetime.now())
        if response_order.get("code") == '201':
            exec_data.append((purchase_number,'Y',modify_time,response_order))
        else:
            exec_data.append((purchase_number, 'N', modify_time,response_order))
    for exec in exec_data:
        exec_log = json.dumps(exec[3], ensure_ascii=False)
        sql = f"""update lingxing_purchase_product set data_status='{exec[1]}',modify_time='{exec[2]}',sent_execute_log='{exec_log}' where purchase_number='{exec[0]}'"""
        cursor.execute(sql)
        conn.commit()
    cursor.close()

def lingxing_data_processing(batch_number):
    conn = public_utils.get_mysql('sharkbox_merge')
    one_sub_item(conn,batch_number)
    public_utils.result_write("lingxing_purchase_product", batch_number)
    conn.close()

lingxing_data_processing('f42f7f51-5794-4b56-9e7d-5bd9a3d65b98')