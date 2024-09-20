#!/bin/bash

source_db=$1
source_table=$2
target_db=$3
target_table=$4

. /project_code/code/moyc_lzhl/wms/sqoop_utils/table_columns.sh

sqoop import \
--connect "jdbc:sqlserver://192.168.1.42\SQLEXPRESS;username=sa;password=meio123456;database=${source_db}" \
--hive-import \
--hive-overwrite \
--input-null-string '\\N' \
--input-null-non-string '\\N' \
--fields-terminated-by ',' \
--table ${source_table} \
--hive-database ${target_db} \
--hive-table ${target_table} \
--columns ${table_columns} \
--num-mappers 1
