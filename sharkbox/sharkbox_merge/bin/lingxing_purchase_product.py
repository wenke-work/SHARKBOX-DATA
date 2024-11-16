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
    url = "http://%s/openApi/purchase/saveData" % (host)
    payload = json.dumps(para)
    print(payload)
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

def call_proc(conn):
    cursor = conn.cursor()
    cursor.callproc('proc_lingxing_purchase_product')
    cursor.close()

def one_sub_item(conn,batch_number):
    exec_data = []
    cursor = conn.cursor()
    sql = f'''select purchaser_party,purchase_create_time,purchase_currency,shipping_fee,is_include_tax,total_price_and_tax,cases,expected_delivery_time,product_remarks
                   ,product_name,quantity_per_box,unit_price_including_tax,order_quantity,sku,supplier,purchase_number,other_expenses,transactions
                   ,purchaser,document_remarks,settlement_period,cost_allocation_method,tax_rate,purchase_type,purchase_warehouse,logistics_provider,logistics_tracking_number,order_number_1688
            from lingxing_purchase_product where ifnull(data_status,"")<>"Y" and data_number=1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    for purchaser_party,purchase_create_time,purchase_currency,shipping_fee,is_include_tax,total_price_and_tax,cases,expected_delivery_time,product_remarks,product_name,quantity_per_box,unit_price_including_tax,order_quantity,sku,supplier,purchase_number,other_expenses,transactions,purchaser,document_remarks,settlement_period,cost_allocation_method,tax_rate,purchase_type,purchase_warehouse,logistics_provider,logistics_tracking_number,order_number_1688 in result:
        sub_para ={
                      "amount": none_to_string(total_price_and_tax),
                      "boxCount": none_to_string(cases),
                      "eta": none_to_string(expected_delivery_time),
                      "lineRemark": none_to_string(product_remarks),
                      "name": none_to_string(product_name),
                      "perboxqty": none_to_string(quantity_per_box),
                      "price": none_to_string(unit_price_including_tax),
                      "purchaseQuantity": none_to_string(order_quantity),
                      "sku": none_to_string(sku),
                      "supplier": none_to_string(supplier)
            }
        sub_list = []
        sub_list.append(sub_para)
        para_data = {
                      "alibabaOrderId": none_to_string(order_number_1688),
                      "amount": none_to_string(total_price_and_tax),
                      "buyer": none_to_string(purchaser_party),
                      "contactMethod": "",
                      "contacts": "",
                      "createTime": none_to_string(purchase_create_time),
                      "currency": none_to_string(purchase_currency),
                      "freight": none_to_string(shipping_fee),
                      "isTax": none_to_string(is_include_tax),
                      "customerOrderNo": none_to_string(purchase_number),
                      "otherCost": none_to_string(other_expenses),
                      "payMethod": none_to_string(transactions),
                      "purchaser": none_to_string(purchaser),
                      "remark": none_to_string(document_remarks),
                      "settlementMethod": none_to_string(settlement_period),
                      "shareMethod": none_to_string(cost_allocation_method),
                      "supplier": none_to_string(supplier),
                      "taxRate": none_to_string(tax_rate),
                      "type": none_to_string(purchase_type),
                      "updateTime": none_to_string(purchase_create_time),
                      "warehouseName": none_to_string(purchase_warehouse),
                      "items": sub_list
            }
        response = call_api(para_data)
        modify_time = str(datetime.now())
        if response.get("code") == '201':
            exec_data.append((purchase_number,'Y',modify_time,response))
        else:
            exec_data.append((purchase_number,'N',modify_time,response))
    for exec in exec_data:
        exec_log = json.dumps(exec[3], ensure_ascii=False)
        sql = f"""update lingxing_purchase_product set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where purchase_number='{exec[0]}'"""
        cursor.execute(sql)
        conn.commit()
    cursor.close()

def many_sub_item(conn,batch_number):
    cursor = conn.cursor()
    sql = f'''select distinct purchase_number as purchase_number from lingxing_purchase_product where data_status<>"Y" and data_number>1 and batch_number="{batch_number}"'''
    cursor.execute(sql)
    result = cursor.fetchall()
    for resu in result:
        purchase_number = resu[0]
        sql = f'''select purchaser_party,purchase_create_time,purchase_currency,shipping_fee,is_include_tax,total_price_and_tax,cases,expected_delivery_time,product_remarks
                       ,product_name,quantity_per_box,unit_price_including_tax,order_quantity,sku,supplier,purchase_number,other_expenses,transactions
                       ,purchaser,document_remarks,settlement_period,cost_allocation_method,tax_rate,purchase_type,purchase_warehouse,logistics_provider,logistics_tracking_number,order_number_1688
                from lingxing_purchase_product where data_status<>"Y" and purchase_number="{purchase_number}" and batch_number="{batch_number}"'''
        cursor.execute(sql)
        result_many = cursor.fetchall()
        sub_list = []
        modify_time = str(datetime.now())
        num = 0
        for purchaser_party,purchase_create_time,purchase_currency,shipping_fee,is_include_tax,total_price_and_tax,cases,expected_delivery_time,product_remarks,product_name,quantity_per_box,unit_price_including_tax,order_quantity,sku,supplier,purchase_number,other_expenses,transactions,purchaser,document_remarks,settlement_period,cost_allocation_method,tax_rate,purchase_type,purchase_warehouse,logistics_provider,logistics_tracking_number,order_number_1688 in result_many:
            sub_para = {
                    "amount": none_to_string(total_price_and_tax),
                    "boxCount": none_to_string(cases),
                    "eta": none_to_string(expected_delivery_time),
                    "lineRemark": none_to_string(product_remarks),
                    "name": none_to_string(product_name),
                    "perboxqty": none_to_string(quantity_per_box),
                    "price": none_to_string(unit_price_including_tax),
                    "purchaseQuantity": none_to_string(order_quantity),
                    "sku": none_to_string(sku),
                    "supplier": none_to_string(supplier)
            }
            sub_list.append(sub_para)
            num = num + 1
            if len(result_many) == num:
                para_data = {
                    "alibabaOrderId": none_to_string(order_number_1688),
                    "amount": none_to_string(total_price_and_tax),
                    "buyer": none_to_string(purchaser_party),
                    "contactMethod": "",
                    "contacts": "",
                    "createTime": none_to_string(purchase_create_time),
                    "currency": none_to_string(purchase_currency),
                    "freight": none_to_string(shipping_fee),
                    "isTax": none_to_string(is_include_tax),
                    "customerOrderNo": none_to_string(purchase_number),
                    "otherCost": none_to_string(other_expenses),
                    "payMethod": none_to_string(transactions),
                    "purchaser": none_to_string(purchaser),
                    "remark": none_to_string(document_remarks),
                    "settlementMethod": none_to_string(settlement_period),
                    "shareMethod": none_to_string(cost_allocation_method),
                    "supplier": none_to_string(supplier),
                    "taxRate": none_to_string(tax_rate),
                    "type": none_to_string(purchase_type),
                    "updateTime": none_to_string(purchase_create_time),
                    "warehouseName": none_to_string(purchase_warehouse),
                    "items": sub_list
                }
                response = call_api(para_data)
                if response.get("code") == '201':
                    exec = [purchase_number, 'Y', modify_time,response]
                else:
                    exec = [purchase_number,'N',modify_time,response]
                exec_log = json.dumps(exec[3], ensure_ascii=False)
                sql = f"""update lingxing_purchase_product set data_status='{exec[1]}',modify_time='{exec[2]}',execute_log='{exec_log}' where purchase_number='{exec[0]}'"""
                cursor.execute(sql)
                conn.commit()
    cursor.close()

def lingxing_data_processing(batch_number):
    conn = public_utils.get_mysql('sharkbox_merge')
    call_proc(conn)
    one_sub_item(conn,batch_number)
    many_sub_item(conn,batch_number)
    conn.close()

#lingxing_data_processing('e96f4804-b6d6-4a15-bd04-e239a82289d3')