#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, time, sys
import threading
from datetime import datetime
import multiprocessing

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
sys.path.append(parent_directory + '/utils')
sys.path.append(parent_directory + '/kafka_execute')
import actuator_conf
import kafka_utils_public

# topic名
topic_name = sys.argv[1]
# 消费组group_id
group_name = sys.argv[2]
# 日志记录的表名及执行的python模块名
log_table = sys.argv[3]


# 根据变量名导入模块
module_import = __import__(log_table)
# 绑定模块的data_processing函数
exec_api_program = getattr(module_import,"data_processing")

# 每次收到消息初始化一个dict记录程序执行状态
def get_dict():
    global_dict = {}
    global_dict['exec_step'] = ""
    global_dict['exec_code'] = -1
    global_dict['exec_status'] = ""
    global_dict['exec_time'] = str(datetime.now())
    return global_dict

# 在主线程中开启一个线程执行操作，主线程负责监听执行状态
def message_processing(message):
    global_dict = get_dict()
    try:
        # 解析消息并将消息存入到字典
        di = kafka_utils_public.parsing_messages(message)
        global_dict.update(di)
        # 开启线程来执行调用API写数据
        thread_api = threading.Thread(target=exec_api_program, args=(global_dict,))
        thread_api.start()
        wail = 0
        # 主线程查询子线程执行状态，未执行完成等待0.1秒，等待时间不超过30秒
        while wail < 30:
            if global_dict['exec_code'] == -1:
                time.sleep(0.1)
                wail += 0.1
            else:
                break
        # 判断执行结果，未成功发送消息
        if global_dict['exec_code'] != 200 and global_dict['exec_code'] != 0:
            if global_dict['exec_code'] == -1:
                global_dict['exec_step'] = "fail : %s 接口超过30秒无返回值,进程自杀了,亲..."%(log_table)
            kafka_utils_public.sent_to_wechat(global_dict)
    except Exception as e:
        global_dict['exec_step'] = "调用API前-执行报错"
        kafka_utils_public.sent_to_wechat(global_dict)
    finally:
        # 记录数据库
        kafka_utils_public.write_mysql(global_dict,log_table)
        os.kill(os.getpid(), 9)

# 消费center topic的消息，每次获取一条，开起一个进程处理这一条数据，当数据处理完后再重新消费
if __name__ == "__main__":
    # 获取consumer
    consumer = actuator_conf.get_consumer(topic_name,group_name)
    for message in consumer:
        if message:
            p = multiprocessing.Process(target=message_processing, args=(message,))
            p.start()
            p.join()