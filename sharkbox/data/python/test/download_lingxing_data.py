import json

import requests,time,sys
from openapi_sdk import sign
from urllib.parse import quote
import pyodbc
from datetime import datetime

app_id = "ak_YiHZ9hYITu2dG"
app_secret = "e6qB3g0HGFu7VanrKr++7w=="

current_time = int(time.time())

# 参数
body_para = {}
if len(sys.argv) >= 2:
    body_para["offset"] = int(sys.argv[1])
if len(sys.argv) >= 3:
    body_para["length"] = int(sys.argv[2])
if len(sys.argv) >= 4:
    time_update_start = time.strptime(sys.argv[3], "%Y-%m-%d")
    body_para["update_time_start"] = int(time.mktime(time_update_start))
if len(sys.argv) >= 5:
    time_update_end = time.strptime(sys.argv[4], "%Y-%m-%d")
    body_para["update_time_end"] = int(time.mktime(time_update_end))
if len(sys.argv) >= 6:
    time_create_start = time.strptime(sys.argv[5], "%Y-%m-%d")
    body_para["create_time_start"] = int(time.mktime(time_create_start))
if len(sys.argv) >= 7:
    time_create_end = time.strptime(sys.argv[6], "%Y-%m-%d")
    body_para["create_time_end"] = int(time.mktime(time_create_end))
if len(sys.argv) >= 8:
    body_para["sku_list"] = sys.argv[7]
print(body_para)

#获取token
def get_access_token():
    url = "https://openapi.lingxing.com/api/auth-server/oauth/access-token"
    files = {'file' : b''}
    data = {
        "appId": app_id,
        "appSecret": app_secret
    }
    response = requests.post(url, files=files,data=data)
    return response.json().get("data").get("access_token")

def para_process():
    conn = get_sql_server('kettle')
    cursor = conn.cursor()
    cursor.execute('SELECT TOP 1 update_time_end,create_time_end FROM sharkbox_data.dbo.lingxing_token ORDER BY id DESC')
    result = cursor.fetchall()
    update_end = result[0][0]
    create_end = result[0][1]
    body_para["offset"] = body_para.get("offset",0)
    body_para["length"] = body_para.get("length", 1000)
    body_para["update_time_start"] = body_para.get("update_time_start", update_end)
    body_para["update_time_end"] = body_para.get("update_time_end", current_time)
    body_para["create_time_start"] = body_para.get("create_time_start", create_end)
    body_para["create_time_end"] = body_para.get("create_time_end", current_time)
    return conn

# 签名算法
def get_sign(access_token):
    data = {
        "access_token":access_token,
        "app_key":app_id,
        "timestamp":current_time
    }
    c_data = data.copy()
    c_data.update(body_para)
    data_di = {key: c_data[key] for key in sorted(c_data, key=lambda item: item)}
    print(data_di)
    sign_data = sign.SignBase.generate_sign(app_id, data_di)
    data["sign"] = quote(sign_data)
    return data

def lists(para_data,conn):
    url = "https://openapi.lingxing.com/erp/sc/routing/data/local_inventory/productList"
    para=''
    for key,value in para_data.items():
        para = para + str(key) + "=" + str(value) + "&"
    para = para[:-1]
    url = url + "?" + para
    js_para=json.dumps(body_para)
    sql = f"""insert into sharkbox_data.dbo.lingxing_token values('{para_data.get("access_token")}'
                                                                 ,'{para_data.get("sign")}'
                                                                 ,'{para_data.get("timestamp")}'
                                                                 ,'{url}'
                                                                 ,{body_para["offset"]}
                                                                 ,{body_para["length"]}
                                                                 ,{body_para["update_time_start"]}
                                                                 ,{body_para["update_time_end"]}
                                                                 ,{body_para["create_time_start"]}
                                                                 ,{body_para["create_time_end"]}
                                                                 ,'{body_para.get("sku_list")}'
                                                                 ,'{js_para}'
                                                                 ,getdate()
                                                                 )"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url,headers=headers,data=json.dumps(body_para))
    data = response.json().get("data")
    num = 0
    print(response.json())
    for line_data in data:
        print(line_data)
        num = num + 1
    print(response.json().get("total"))
    print(num)


def get_sql_server(database):
    if database == 'kettle':
        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=106.55.145.65;'
            r'DATABASE=sharkbox_data;'
            r'UID=sa;'
            r'PWD=csSK[wKh6@jy999;'
        )
        conn = pyodbc.connect(conn_str)
        return conn

access_token = get_access_token()
conn = para_process()
para_data = get_sign(access_token)
lists(para_data,conn)


