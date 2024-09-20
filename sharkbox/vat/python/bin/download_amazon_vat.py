#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyodbc
import paramiko

def get_sql_server(database):
    if database == 'vat':
        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=106.53.113.34;'
            r'DATABASE=vat_db;'
            r'UID=sa;'
            r'PWD=meio$thiierdeSuc$u;'
        )
        conn = pyodbc.connect(conn_str)
        return conn

def get_ssh():
    # 建立SSH连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="106.55.145.65", port=22, username="Administrator", password="sLfaV5@8(YAN")
    return ssh

if __name__ == "__main__":
    sql = '''select distinct t2.F_FilePath from
                (select SalesDataTableId from testvat_db.dbo.UploadSalesData where SalesPlatformId=3) t1
            left join
                (select F_FilePath,InfoId from testvat_db.dbo.Base_AnnexesFile where InfoId is not null) t2
            on t1.SalesDataTableId=t2.InfoId'''

    conn = get_sql_server('vat')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    ssh = get_ssh()
    sftp = ssh.open_sftp()

    for file_path in result:
        remote_file = file_path[0]
        local_file = '/tmp/vat_excel/' + remote_file.split('/')[-1]
        sftp.get(remote_file,local_file)

    sftp.close()
    ssh.close()
    cursor.close()
    conn.close()