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
host='192.168.1.27:8081'

def none_to_string(value):
    return "" if value is None else str(value)

def call_api(para):
    url = "http://%s/openApi/auth/saveAuth" % (host)
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
        return {'code': '1', 'msg': '调用接口时程序报错'}

def lingxing_data_processing(batch_number):
    exec_data = []
    conn = public_utils.get_mysql('sharkbox_merge')
    cursor = conn.cursor()
    sql = f'select account_name,advertisement_authorize,country,seller_id,store_authorize,update_authorize_time from lingxing_merchantlist where data_status<>"Y"  and batch_number="{batch_number}" '
    cursor.execute(sql)
    result = cursor.fetchall()
    for account_name,advertisement_authorize,country,seller_id,store_authorize,update_authorize_time in result:
        para = {
                  "accountName": none_to_string(account_name),
                  "advertisementAuthorize": none_to_string(advertisement_authorize),
                  "country": none_to_string(country),
                  "sellerId": none_to_string(seller_id),
                  "storeAuthorize": none_to_string(store_authorize),
                  "updateAuthorizeTime": none_to_string(update_authorize_time)
            }
        response = call_api(para)
        modify_time = str(datetime.now())
        if response.get("code") == '201':
            exec_data.append((seller_id,country,'Y',modify_time,response))
        else:
            exec_data.append((seller_id,country,'N',modify_time,response))
    for exec in exec_data:
        exec_log = json.dumps(exec[4], ensure_ascii=False)
        sql = f"""update lingxing_merchantlist set data_status='{exec[2]}',modify_time='{exec[3]}',execute_log='{exec_log}' where seller_id='{exec[0]}' and country='{exec[1]}'"""
        cursor.execute(sql)
        conn.commit()
    public_utils.result_write("lingxing_merchantlist",batch_number)
    cursor.close()
    conn.close()

#lingxing_data_processing('6b6a770e-4eff-4913-920d-5ce40514d875')