#!/usr/bin/python
# -*- coding: utf-8 -*-

import kafka_call_api_wms

#执行程序调API
def data_processing(global_dict):
    try:
        # 获取center指定的操作表
        business = global_dict.get("kafka_value").get("table")
        # 执行仓库新增
        if business == "SKU":
            sku_code = global_dict.get("kafka_value").get("data").get("code")
            warehouse_list = global_dict.get("kafka_value").get("data").get("warehouseID").split(",")
            for id,warehouse_id in enumerate(warehouse_list):
                add_goods_response = kafka_call_api_wms.to_wms_add_goods(global_dict,warehouse_id)
                if add_goods_response.get("code") == 200:
                    global_dict['exec_step'] += "[success : oms to wms SKU信息 sku:%s , 仓库id：%s , 接口返回信息：%s]  "%(sku_code,warehouse_id,add_goods_response.get("info"))
                else:
                    global_dict['exec_step'] += "[fail : oms to wms SKU信息 sku:%s , 仓库id：%s , 接口返回信息：%s]  "%(sku_code,warehouse_id,add_goods_response.get("info"))

                # 判断是否执行完成最后一个地址
                if id == len(warehouse_list)-1:
                    if global_dict['exec_step'].find("fail") == -1:
                        global_dict['exec_code'] = 200
                    else:
                        global_dict['exec_code'] = 1
        else:
            global_dict['exec_step'] = "这条数据不需要推送WMS"
            global_dict['exec_code'] = 0
    except Exception as e:
        global_dict['exec_step'] = "oms to wms调用API-执行报错"
        global_dict['exec_code'] = 2