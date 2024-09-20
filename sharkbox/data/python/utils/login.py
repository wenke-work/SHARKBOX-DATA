#!/usr/bin/python

import requests
import json


def login_to_wms(session):
    url = "http://192.168.1.42:81/meio/User/login"
    payload = json.dumps({
        "userName": "wuwenke",
        "password": "wuwenke"
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = session.post(url, headers=headers, data=payload)
    if response.json().get("code") == 200:
        return "登录成功"
    else:
        return "登录失败！"


def login_to_center(session):
    url = "http://192.168.1.45:2234/api/SignIn/Post?userName=admin&pwd=123"
    response = session.get(url)
    token = response.json().get('Token')
    if response.json().get('Success') == True:
        return "登录成功",token
    else:
        return "登录失败！",None
