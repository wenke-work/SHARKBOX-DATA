create table if not exists ods_1688.ods_product_category(
     id                string COMMENT '类目ID'
    ,name              string COMMENT '类目名称'
    ,is_leaf           string COMMENT '是否叶子类目（只有叶子类目才能发布商品）'
    ,category_type     string COMMENT '类目的类型，1为1688大市场类目，2为1688工业品专业化类目，3为1688主流商品类目'
    ,super_id          string COMMENT '父类目ID'
)
comment '根据类目Id查询类目--com.alibaba.product:alibaba.category.get-1'
row format delimited fields terminated by ','
stored as Textfile
;

CREATE TABLE data_1688.ods_product_category(
     id                bigint       COMMENT '类目ID'
    ,name              VARCHAR(255) COMMENT '类目名称'
    ,is_leaf           VARCHAR(255) COMMENT '是否叶子类目（只有叶子类目才能发布商品）'
    ,category_type     int          COMMENT '类目的类型，1为1688大市场类目，2为1688工业品专业化类目，3为1688主流商品类目'
    ,super_id          bigint       COMMENT '父类目ID'
    ,PRIMARY KEY(id)
)COMMENT "根据类目Id查询类目--com.alibaba.product:alibaba.category.get-1"
ENGINE=INNODB CHARSET=utf8;