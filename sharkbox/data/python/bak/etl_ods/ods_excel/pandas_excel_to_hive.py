import pandas as pd
from pyhive import hive
import shutil,os

conn = hive.Connection(host='172.16.0.2',port=10000,database='test')
cursor = conn.cursor()
file_names = os.listdir('/tmp/vat_excel/')
for file_name in file_names:
    source_data = '/tmp/vat_excel/' + file_name
    target_data = source_data.replace('.xlsx','.csv')
    data = pd.read_excel(source_data,engine='openpyxl')
    data.to_csv(target_data,index=False)
    hql = "LOAD DATA LOCAL INPATH '%s' INTO TABLE ods_vat.ods_vat_db_amazonvatsalesdata partition(ds='20240909')" %(target_data)
    cursor.execute(hql)
conn.close()
shutil.rmtree('/tmp/vat_excel/')
os.mkdir('/tmp/vat_excel/')