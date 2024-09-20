#!/usr/bin/python
# -*- coding: utf-8 -*-
#from pyhive import hive

# conn = hive.Connection(host='172.16.0.2',port=10000,database='test')
# # 查询
# cursor = conn.cursor()
# cursor.execute('select * from table_test_3')
# for result in cursor.fetchall():
#     print(result)
st = '/tmp/vat_excel/4effcacf-f60f-4c62-aeb5-0c91e8c56079.xlsx'
hql = "LOAD DATA LOCAL INPATH '%s' INTO TABLE ods_vat.ods_vat_db_amazonvatsalesdata partition(ds='20240909')" %(st)
print(hql)
target_data = st.replace('.xlsx','.csv')
print(target_data)
