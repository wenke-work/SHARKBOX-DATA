#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, requests


# 用于发送消息到企业微信
def transaction_sent_to_wechat(di):
    message = f'''>>>t_id:{di.get("t_id")}\n>>>事务发起方及主方法名:{di.get("main_app")}\n>>>事务创建时间:{di.get("exec_time")}\n>>>事务执行方及执行次数:{di.get("app_name")}-->{di.get("retry_count")}\n>>>执行接口链接:{di.get("app_url")}\n>>>runState状态(4:成功)：{di.get("run_state")}\n>>>接口执行信息：{di.get("result_message")}'''
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b9ff9f6b-748c-4e72-b3f7-a827985e9727"
    payload = json.dumps({"msgtype": "text",
                          "text": {
                              "content": message
                          }})
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)
