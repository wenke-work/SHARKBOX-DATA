#!/bin/bash

case ${source_table} in
'ods_product_category')
    table_columns='id,name,is_leaf,category_type,super_id'
;;
esac