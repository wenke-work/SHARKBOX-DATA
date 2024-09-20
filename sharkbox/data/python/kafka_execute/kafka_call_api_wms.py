#!/usr/bin/python
import json
import requests,logging


host='192.168.1.42:81'
#host='106.55.145.65:89'

# 用于将center接收到的 仓库 信息写入到wms
def to_wms_add_warehouse(global_dict):
    url = "http://%s/meio/BaseData/AddWarehouse"%(host)
    dic = global_dict.get("kafka_value").get("data")
    addr = dic.get("Country")+dic.get("Province")+dic.get("City")+dic.get("Area")+dic.get("Addrss")
    data_di = {
        "ID": dic.get("ID"),
        "Code": dic.get("Code"),
        "Name": dic.get("Name"),
        "Addr": addr,
        "LinkMan": dic.get("PersonCharge"),
        "Tel": dic.get("Telphone"),
        "Phone": dic.get("Telphone")
    }
    payload = json.dumps({"action": global_dict.get("kafka_value").get("action"),
                          "data": data_di})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

# 用于将center接收到的 货主 信息写入到wms
def to_wms_add_shipper(global_dict,warehouse_id):
    url = "http://%s/meio/BaseData/AddShipper"%(host)
    dic = global_dict.get("kafka_value").get("data")
    data_di = {
        "ID": dic.get("ID"),
        "Code": dic.get("Code"),
        "Name": dic.get("Name"),
        "EnName": "",
        "Addr": "",
        "LinkMan": "",
        "Tel": "",
        "Phone": "",
        "Enabled": dic.get("IsValid"),
        "WarehouseID": warehouse_id
    }

    payload = json.dumps({"action": global_dict.get("kafka_value").get("action"),
                          "data": data_di})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

# 用于将oms接收到的 sku 信息写入到wms
def to_wms_add_goods(global_dict,warehouse_id):
    url = "http://%s/meio/BaseData/AddGoods"%(host)
    dic = global_dict.get("kafka_value").get("data")
    data_di = {
        "System": global_dict.get("kafka_value").get("system"),
        "Code": dic.get("code"),
        "CodeKey": "",
        "BjCode": "",
        "BjID": "",
        "ShipperID": dic.get("shipperId"),
        "ShipperName": "",
        "Brand": dic.get("brand"),
        "Name": dic.get("name"),
        "EnName": "",
        "Specifications": dic.get("specifications"),
        "Colour": "",
        "Size": "",
        "Lenght": dic.get("lenght"),
        "Width": dic.get("width"),
        "Height": dic.get("height"),
        "Volume": dic.get("volume"),
        "Weight": dic.get("weight"),
        "Type": dic.get("type"),
        "Imgs": dic.get("imgs"),
        "WarehouseID": warehouse_id,
        "Operatingfee": 0,
        "Costprice": 0,
        "IsNewProduct": dic.get("isNewProduct"),
        "electron": dic.get("electron"),
        "FNSKU": dic.get("fnsku"),
        "Attribute1": "",
        "Attribute2": "",
        "Price": dic.get("price"),
        "SendType": dic.get("sendType"),
        "Enabled":dic.get("enabled")
    }
    payload = json.dumps({"action": global_dict.get("kafka_value").get("action"),
                          "data": data_di})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()