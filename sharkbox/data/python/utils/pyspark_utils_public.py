#!/usr/bin/python
# -*- coding: utf-8 -*-

import hmac,hashlib,json


app_secret = 'BO31M7ntnIyH'

# 用于1688的签名算法
def encryption1688(signatureStr):
    key = app_secret.encode('utf-8')
    message = signatureStr.encode('utf-8')
    hmac_obj = hmac.new(key,message,digestmod=hashlib.sha1)
    hmac_value = hmac_obj.hexdigest()
    return hmac_value.upper()

# 用于1688签名算法的参数拼接
def paramHandle1688(params):
    paramList = []
    for key,value in params.items():
        s = str(key)+str(value)
        paramList.append(s)
    return ''.join(sorted(paramList))

# 用于将数据写入到本地
def writerPyspark(path,global_list):
    with open(path,"a",encoding="utf-8") as f:
        for data in global_list:
            data_json = json.dumps(data,ensure_ascii=False)
            f.write(data_json+'\n')