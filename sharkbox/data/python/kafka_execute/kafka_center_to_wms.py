#!/usr/bin/python
# -*- coding: utf-8 -*-

import kafka_call_api_wms

#执行程序调API
def data_processing(global_dict):
    try:
        # 获取center指定的操作表
        business = global_dict.get("kafka_value").get("table")
        # 执行仓库新增
        if business == "warehouse":
            warehouse_id=global_dict.get("kafka_value").get("data").get("ID")
            add_warehouse_response = kafka_call_api_wms.to_wms_add_warehouse(global_dict)
            if add_warehouse_response.get("code") == 200:
                global_dict['exec_step'] = "success : center to wms仓库 仓库id : %s , 接口返回信息 ：%s"%(warehouse_id,add_warehouse_response.get("info"))
                global_dict['exec_status'] = add_warehouse_response.get("info")
                global_dict['exec_code'] = add_warehouse_response.get("code")
            else:
                global_dict['exec_step'] = "fail : center to wms仓库 仓库id : %s , 接口返回信息 ：%s"%(warehouse_id,add_warehouse_response.get("info"))
                global_dict['exec_status'] = add_warehouse_response.get("info")
                global_dict['exec_code'] = add_warehouse_response.get("code")
        # 执行货主新增
        elif business == "owner":
            # 获取货主id
            owner_id = global_dict.get("kafka_value").get("data").get("ID")
            # 获取货主名下的仓库地址
            warehouse_list = global_dict.get("kafka_value").get("data").get("WarehouseID").split(",")
            for id,warehouse_id in enumerate(warehouse_list):
                #将货主信息写入到仓库
                add_response = kafka_call_api_wms.to_wms_add_shipper(global_dict,warehouse_id)
                if add_response.get("code") == 200:
                    global_dict['exec_step'] += "[success : center to wms货主 货主id：%s , 仓库id：%s , 接口返回信息 ：%s] "%(owner_id,warehouse_id,add_response.get("info"))
                else:
                    global_dict['exec_step'] += "[fail : center to wms货主 货主id：%s , 仓库id：%s , 接口返回信息 ：%s] "%(owner_id,warehouse_id,add_response.get("info"))

                # 判断是否执行完成最后一个地址
                if id == len(warehouse_list)-1:
                    if global_dict['exec_step'].find("fail") == -1:
                        global_dict['exec_code'] = 200
                    else:
                        global_dict['exec_code'] = 1
        # 包材
        elif business == "SKU":
            sku_code = global_dict.get("kafka_value").get("data").get("code")
            warehouse_list = global_dict.get("kafka_value").get("data").get("warehouseID").split(",")
            for id,warehouse_id in enumerate(warehouse_list):
                add_goods_response = kafka_call_api_wms.to_wms_add_goods(global_dict,warehouse_id)
                if add_goods_response.get("code") == 200:
                    global_dict['exec_step'] += "[success : center to wms 包材 sku:%s , 仓库id：%s , 接口返回信息：%s]  "%(sku_code,warehouse_id,add_goods_response.get("info"))
                else:
                    global_dict['exec_step'] += "[fail : center to wms 包材 sku:%s , 仓库id：%s , 接口返回信息：%s]  "%(sku_code,warehouse_id,add_goods_response.get("info"))

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
        global_dict['exec_step'] = "center to wms调用API-执行报错"
        global_dict['exec_code'] = 2