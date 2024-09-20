#!/usr/bin/python
# -*- coding: utf-8 -*-

import json,os,sys,requests
import time
import threading
import multiprocessing

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
sys.path.append(parent_directory + '/utils')
sys.path.append(parent_directory + '/kafka_execute')
import actuator_conf
import utils_public

running = True

# 程序休息时间
sleep_second = int(sys.argv[1])
# 执行间隔时间
interval_second = int(sys.argv[2])

def call_api(di_exec,url,headers,para):
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(para), timeout=(10,20))
        di_exec['result_message'] = response.json()
    except requests.exceptions.Timeout as e:
        di_exec['result_message'] = 'requests.exceptions.Timeout: 请求超时'
    except Exception as e:
        di_exec['result_message'] = '调用API时报错'

if __name__ == "__main__":
    # 获取数据库链接
    while True:
        con = actuator_conf.get_mysql('sharkbox_transaction')
        sql="select t_id,call_info,retry_count,create_time from global_transaction where main_state=2 and TIMESTAMPDIFF(SECOND,create_time,NOW()) >= %d" %(interval_second)
        # 执行sql
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        # 定义一个进程池, 最大进程数4
        # p = multiprocessing.Pool(2)
        for t_id,call_info,retry_count,create_time in result:
            di_exec = {}
            api_state = ''
            try:
                di_exec["t_id"] = t_id
                di_exec["retry_count"] = retry_count + 1
                di_exec["exec_time"] = create_time
                dic_call_info = json.loads(call_info)
                di_exec["main_app"] = dic_call_info.get("mainAPP") + '-->' + dic_call_info.get("callMethod")
                api_list = dic_call_info.get('apis')
                for api in api_list:
                    di_exec["app_name"] = api.get('appName')
                    di_exec["app_url"] = api.get('url')
                    di_exec["run_state"] = api.get('runState')
                    if int(api.get('runState')) != 4:
                        api_state += 'N'
                        url = api.get('url')
                        headers = api.get('headers')
                        headers.update({'User-Agent': 'Apifox/1.0.0 (https://apifox.com)','Content-Type': 'application/json'})
                        paras = api.get('paras')
                        # 开启线程来执行调用API写数据
                        # p.apply_async(call_api,(di_exec,url,headers,paras))
                        thread_api = threading.Thread(target=call_api, args=(di_exec,url,headers,paras))
                        thread_api.start()
                        wail = 0
                        # 主线程查询子线程执行状态，未执行完成等待0.5秒，等待时间不超过30秒
                        while wail < 30:
                            if 'result_message' in di_exec:
                                break
                            else:
                                time.sleep(0.5)
                                wail += 0.5
                    else:
                        api_state += 'Y'
            except:
                api_state += 'N'
                di_exec['result_message'] = '解析json时出错'
            if api_state.find('N') == -1:
                delete_sql = 'delete from global_transaction where t_id = "%s"' %(t_id)
                cursor.execute(delete_sql)
                con.commit()
            else:
                update_sql = 'update global_transaction set retry_count = retry_count + 1,modify_time = now() where t_id = "%s"' %(t_id)
                if (retry_count + 1)%10 == 1:
                    utils_public.transaction_sent_to_wechat(di_exec)
                cursor.execute(update_sql)
                con.commit()
        cursor.close()
        con.close()
        time.sleep(sleep_second)