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

def call_api(para):
    url = "http://%s/openApi/customer/saveAction" % (host)
    payload = json.dumps(para)
    headers = {
        'Content-Type': 'application/json',
        'tenant':'HZ007'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=(10,10))
        return response.json()
    except requests.exceptions.Timeout as e:
        return {'code': '-1', 'msg': 'requests.exceptions.Timeout: 请求超时'}
    except Exception as e:
        return {'code': '1','msg': '调用接口时程序报错'}

def lingxing_data_processing(batch_number):
    exec_data = []
    conn = public_utils.get_mysql('sharkbox_merge')
    cursor = conn.cursor()
    sql = f'select address,qq_wachat,email,contacts,supplier_name,supplier_code,contact_information from lingxing_supplier where data_status<>"Y" and batch_number="{batch_number}"'
    cursor.execute(sql)
    result = cursor.fetchall()
    for address,qq_wachat,email,contacts,supplier_name,supplier_code,contact_information in result:
        contact_info = ''
        if qq_wachat or email:
            contact_info = "qq或微信-" + qq_wachat + ",邮箱-" + email
        para = {
                "address": none_to_string(address),
                "contact_info": contact_info,
                "contacts": none_to_string(contacts),
                "ftype": "0",
                "fullname": none_to_string(supplier_name),
                "name": none_to_string(supplier_name),
                "number": supplier_code,
                "phone_num": none_to_string(contact_information)
            }
        response = call_api(para)
        modify_time = str(datetime.now())
        if response.get("code") == '201':
            exec_data.append((supplier_code,'Y',modify_time,response))
        else:
            exec_data.append((supplier_code,'N',modify_time,response))
    for exec in exec_data:
        exec_log = json.dumps(exec[3],ensure_ascii=False)
        sql = f"""update lingxing_supplier set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where supplier_code='{exec[0]}'"""
        cursor.execute(sql)
        conn.commit()
    public_utils.result_write("lingxing_supplier", batch_number)
    cursor.close()
    conn.close()

#lingxing_data_processing("baeef134-5ea1-4250-b3dd-c86697d0470f")