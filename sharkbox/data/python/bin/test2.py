#!/usr/bin/python
# -*- coding: utf-8 -*-
#from pyhive import hive

# conn = hive.Connection(host='172.16.0.2',port=10000,database='test')
# # 查询
# cursor = conn.cursor()
# cursor.execute('select * from table_test_3')
# for result in cursor.fetchall():
#     print(result)
# st = '/tmp/vat_excel/4effcacf-f60f-4c62-aeb5-0c91e8c56079.xlsx'
# hql = "LOAD DATA LOCAL INPATH '%s' INTO TABLE ods_vat.ods_vat_db_amazonvatsalesdata partition(ds='20240909')" %(st)
# print(hql)
# target_data = st.replace('.xlsx','.csv')
# print(target_data)
# cmd
#------------------------------------------------------------------------------------------------------------------------

#
# import psutil
# cpu_percent = psutil.cpu_percent(interval=1)
# print(cpu_percent)
# cpu_memory = psutil.virtual_memory()
# print(cpu_memory)

#------------------------------------------------------------------------------------------------------------------------
# from datetime import datetime, timedelta
# now = datetime.now()
# one_day_ago = now - timedelta(days=1)
# str_date=one_day_ago.strftime("%Y-%m-%d")
# print(str_date)

#------------------------------------------------------------------------------------------------------------------------
# from pdf2image import convert_from_path
source_data = "C:\\Users\\Administrator\\Desktop\\files\\temp\\test\\身份证正反面.pdf"
source_name = source_data[:-4]
print(source_name)

# images = convert_from_path(source_data)
# for i, image in enumerate(images):
#     image.save(f'{source_data}_{i}.jpg', 'JPEG')