#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
背景 : 需要将领星的数据迁移到我们自己的平台
功能 :1.监听MySQL中需要迁移的数据表,当出现跟新时调用相应处理程序
参数 :
"""

import sys,os
import multiprocessing
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory + '/conf')
import public_utils



def listen_table(cursor):
    sql = 'SELECT batch_number,table_name FROM sharkbox_merge.lingxing_merge_batch_number WHERE (STATUS="处理完成" OR STATUS="挂起")'
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    for batch_number,table_name in result:
        # 绑定模块的lingxing_data_processing函数
        if table_name == "lingxing_purchase_product":
            module_import = __import__("lingxing_purchase_product")
            exec_api_program = getattr(module_import, "lingxing_data_processing")
            p = multiprocessing.Process(target=exec_api_program,args=(batch_number,))
            p.start()
            module_import = __import__("lingxing_purchase_product_sent_status")
            exec_api_program = getattr(module_import, "lingxing_data_processing")
            p = multiprocessing.Process(target=exec_api_program,args=(batch_number,))
            p.start()
        else:
            module_import = __import__(table_name)
            exec_api_program = getattr(module_import, "lingxing_data_processing")
            p = multiprocessing.Process(target=exec_api_program,args=(batch_number,))
            p.start()
    conn.commit()

if __name__ == "__main__":
    conn = public_utils.get_mysql('sharkbox_merge')
    cursor = conn.cursor()
    num = 0
    try:
        while True:
            print(num)
            num = num + 1
            listen_table(cursor)
            time.sleep(10)
    finally:
        conn.close()
