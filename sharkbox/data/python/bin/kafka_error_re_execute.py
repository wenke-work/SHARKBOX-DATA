#!/usr/bin/python
# -*- coding: utf-8 -*-

import json,os,sys
import time
import threading
from datetime import datetime
import multiprocessing

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
sys.path.append(parent_directory + '/utils')
sys.path.append(parent_directory + '/kafka_execute')
import actuator_conf
import kafka_utils_public

# 程序休息时间
sleep_second = int(sys.argv[1])

def get_dict():
    global_dict = {}
    global_dict['exec_step'] = ""
    global_dict['exec_code'] = -1
    global_dict['exec_status'] = ""
    global_dict['exec_time'] = str(datetime.now())
    return global_dict

def re_execute(kafka_offset,kafka_value,exec_api_program,table_name,retry_count):
    global_dict = get_dict()
    try:
        global_dict['kafka_value'] = json.loads(kafka_value)
        # 开启线程来执行调用API写数据
        thread_api = threading.Thread(target=exec_api_program, args=(global_dict,))
        # 设置线程为守护线程
        thread_api.setDaemon(True)
        thread_api.start()
        wail = 0
        # 主线程查询子线程执行状态，未执行完成等待1秒，等待时间不超过30秒
        while wail < 30:
            if global_dict['exec_code'] == -1:
                time.sleep(1)
                wail += 1
            else:
                break
    except Exception as e:
        global_dict['exec_step'] = "重跑 : 调用API前-执行报错"
    finally:
        # 记录数据库
        kafka_utils_public.update_mysql(global_dict,kafka_offset,table_name,retry_count)
    if global_dict['exec_code'] == 0 or global_dict['exec_code'] == 200:
        global_dict['exec_rerun'] = True
        kafka_utils_public.sent_to_wechat(global_dict)

if __name__ == "__main__":
    while True:
        # 定义一个进程池, 最大进程数4
        p = multiprocessing.Pool(1)
        # 需要读取的Kafka执行记录表
        table_list = ['kafka_center_to_wms','kafka_center_to_oms','kafka_oms_to_wms']
        # 获取数据库链接
        con = actuator_conf.get_mysql('kafka_log')
        for table_name in table_list:
            sql="select kafka_offset,kafka_value,retry_count from %s where exec_code not in(200,0) and retry_count<=3"%(table_name)
            # 根据变量名导入模块
            module_import = __import__(table_name)
            # 绑定模块的data_processing函数
            exec_api_program = getattr(module_import, "data_processing")
            # 执行sql
            cursor = con.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            for kafka_offset,kafka_value,retry_count in result:
                p.apply_async(re_execute,(kafka_offset,kafka_value,exec_api_program,table_name,retry_count))
        p.close()
        p.join()
        con.close()
        time.sleep(sleep_second)