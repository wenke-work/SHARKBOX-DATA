#!/usr/bin/python

from pyspark.sql.types import StringType,StructType,StructField,IntegerType

def tableColumn(table_column):
    if table_column == "GetUserWarehouseList":
        schema = StructType([
            StructField('Code'               ,StringType(),True),
            StructField('Name'               ,StringType(),True),
            StructField('Addr'               ,StringType(),True),
            StructField('LinkMan'            ,StringType(),True),
            StructField('Tel'                ,StringType(),True),
            StructField('Phone'              ,StringType(),True),
            StructField('ID'                 ,StringType(),True),
            StructField('Enabled'            ,StringType(),True),
            StructField('CreationDate'       ,StringType(),True),
            StructField('Creation_Id'        ,StringType(),True),
            StructField('CreationName'       ,StringType(),True),
            StructField('ModificationDate'   ,StringType(),True),
            StructField('Modification_Id'    ,StringType(),True),
            StructField('ModificationName'   ,StringType(),True),
            StructField('SortCode'           ,StringType(),True),
            StructField('CompanyCode'        ,StringType(),True),
            StructField('Company_ID'         ,StringType(),True),
            StructField('CompanyFullName'    ,StringType(),True),
            StructField('CompanyName'        ,StringType(),True),
            StructField('PinYin'             ,StringType(),True),
            StructField('PinYinShort'        ,StringType(),True),
            StructField('Auditor_ID'         ,StringType(),True),
            StructField('AuditorName'        ,StringType(),True),
            StructField('AuditStatus'        ,StringType(),True),
            StructField('Base_ShopInfoID'    ,StringType(),True),
            StructField('ShopName'           ,StringType(),True),
            StructField('Workflow_ID'        ,StringType(),True),
            StructField('EditType'           ,StringType(),True)
        ])
        return schema
    elif table_column == "insert_ods_1688_ods_product_category":
        schema = StructType([
            StructField('id'               ,StringType(),True),
            StructField('name'             ,StringType(),True),
            StructField('isLeaf'           ,StringType(),True),
            StructField('categoryType'     ,StringType(),True),
            StructField('super_id'         ,StringType(),True)
        ])
        return schema

