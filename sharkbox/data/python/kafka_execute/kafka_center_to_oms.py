#!/usr/bin/python
# -*- coding: utf-8 -*-

import kafka_call_api_oms

#执行程序调API
def data_processing(global_dict):
    try:
        # 获取center指定的操作表
        business = global_dict.get("kafka_value").get("table")
        # 货主信息推送oms
        if business == "owner":
            # 获取货主id
            owner_id = global_dict.get("kafka_value").get("data").get("ID")
            add_warehouse_response = kafka_call_api_oms.to_oms_add_shipper(global_dict)
            if add_warehouse_response.get("code") == 200:
                global_dict['exec_step'] = "[success : center to oms货主 货主id：%s , 接口返回信息：%s] "%(owner_id,add_warehouse_response.get("msg"))
                global_dict['exec_status'] = add_warehouse_response.get("info")
                global_dict['exec_code'] = add_warehouse_response.get("code")
            else:
                global_dict['exec_step'] = "[fail : center to oms货主 货主id：%s , 接口返回信息：%s] "%(owner_id,add_warehouse_response.get("msg"))
                global_dict['exec_status'] = add_warehouse_response.get("info")
                global_dict['exec_code'] = add_warehouse_response.get("code")
        else:
            global_dict['exec_step'] = "这条数据不需要推送OMS"
            global_dict['exec_code'] = 0
    except Exception as e:
        global_dict['exec_step'] = "center to oms调用API-执行报错"
        global_dict['exec_code'] = 2