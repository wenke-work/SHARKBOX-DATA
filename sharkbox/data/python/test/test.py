import json

import requests,time,sys
from openapi_sdk import sign
from urllib.parse import quote
import pyodbc
from datetime import datetime

app_id = "ak_YiHZ9hYITu2dG"
app_secret = "e6qB3g0HGFu7VanrKr++7w=="

# topic名
#body_para = sys.argv[1]
body_para = '{"offset": 0,"length": 1000}'



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

# 签名算法
def get_sign(access_token):
    data = {
        "access_token":access_token,
        "app_key":app_id,
        "timestamp":int(time.time()),
    }
    di = json.loads(body_para)
    c_data = data.copy()
    c_data.update(di)
    data_di = {key: c_data[key] for key in sorted(c_data, key=lambda item: item)}
    print(data_di)
    sign_data = sign.SignBase.generate_sign(app_id, data_di)
    data["sign"] = quote(sign_data)
    return data

def lists(para_data):
    url = "https://openapi.lingxing.com/erp/sc/routing/data/local_inventory/productList"
    para=''
    for key,value in para_data.items():
        para = para + str(key) + "=" + str(value) + "&"
    para = para[:-1]
    url = url + "?" + para
    print(url)
    conn = get_sql_server('kettle')
    sql = f"""update sharkbox_data.dbo.lingxing_token set token='{para_data.get("sign")}'
                                                         ,sign='{para_data.get("sign")}'
                                                         ,timestamp='{para_data.get("timestamp")}'
                                                         ,url='{url}'
                                                         ,modify_date=getdate()"""
    print(sql)
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
    response = requests.post(url,headers=headers,data=body_para)
    data = response.json().get("data")
    for line_data in data:
        print(line_data)


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
para_data = get_sign(access_token)
lists(para_data)


