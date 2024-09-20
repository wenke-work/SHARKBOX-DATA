#!/bin/bash

source_db=$1
source_table=$2
target_db=$3
target_table=$4
key=$5

. /project_code/code/moyc_lzhl/data/sqoop_utils/table_columns.sh

sqoop export \
--connect "jdbc:mysql://192.168.117.12:3306/${target_db}?characterEncoding=utf-8" \
--username root \
--password "lzhl@888" \
--export-dir "/user/hive/warehouse/${source_db}.db/${source_table}" \
--table ${target_table} \
--columns ${table_columns} \
--update-key ${key} \
--update-mode allowinsert \
--input-null-string '\\N' \
--input-null-non-string '\\N' \
--input-fields-terminated-by ','
