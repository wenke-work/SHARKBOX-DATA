#!/usr/bin/python
import json
import requests


#host='106.53.113.34:8085'
host='192.168.1.48:8085'

# 用于将center接收到的 仓库 信息写入到oms
def to_oms_add_shipper(global_dict):
    dic = global_dict.get("kafka_value").get("data")
    list_warehouse = []
    list_services = []
    for di in dic.get("Warehouses"):
        warehouse_tmp = {}
        warehouse_tmp["id"] = di.get("ID")
        warehouse_tmp["code"] = di.get("Code")
        warehouse_tmp["name"] = di.get("Name")
        warehouse_tmp["telphone"] = di.get("Telphone")
        warehouse_tmp["addrss"] = di.get("Addrss")
        warehouse_tmp["personCharge"] = di.get("PersonCharge")
        warehouse_tmp["type"] = di.get("Type")
        warehouse_tmp["typeName"] = di.get("TypeName")
        warehouse_tmp["country"] = di.get("Country")
        warehouse_tmp["province"] = di.get("Province")
        warehouse_tmp["city"] = di.get("City")
        warehouse_tmp["area"] = di.get("Area")
        warehouse_tmp["zipCode"] = di.get("ZipCode")
        warehouse_tmp["isValid"] = di.get("IsValid")
        warehouse_tmp["remark"] = di.get("Remark")
        list_warehouse.append(warehouse_tmp)

    for di in dic.get("contractDetailValueAddedServices"):
        service_tmp = {}
        service_tmp["id"] = di.get("ID")
        service_tmp["itemId"] = di.get("ItemID")
        service_tmp["itemName"] = di.get("ItemName")
        service_tmp["itemDetailName"] = di.get("ItemDetailName")
        service_tmp["price"] = di.get("Price")
        service_tmp["contractPrice"] = di.get("ContractPrice")
        service_tmp["discount"] = di.get("Discount")
        service_tmp["unit"] = di.get("Unit")
        service_tmp["priceSheetType"] = di.get("PriceSheetType")
        service_tmp["operationPoint"] = di.get("OperationPoint")
        list_services.append(service_tmp)

    url = "http://%s/admin/api/v1/cargo-owner/add" %(host)

    payload = json.dumps({
        "id": dic.get("ID"),
        "code": dic.get("Code"),
        "name": dic.get("Name"),
        "accountNumber": dic.get("AccountNumber"),
        "password": dic.get("Password"),
        "serviceStartDate": dic.get("ServiceStartDate"),
        "serviceEndDate": dic.get("ServiceEndDate"),
        "dbUrl": dic.get("DbUrl"),
        "dbIp": dic.get("DbIp"),
        "dbPort": dic.get("DbPort"),
        "dbName": dic.get("DbName"),
        "dbUsername": dic.get("DbUsername"),
        "dbPassword": dic.get("DbPassword"),
        "isValid": dic.get("IsValid"),
        "remark": dic.get("Remark"),
        "contractId": dic.get("ContractID"),
        "warehouseId": dic.get("WarehouseID"),
        "warehouses": list_warehouse,
        "servers": list_services
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()