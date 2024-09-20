create table if not exists ods_vat.ods_vat_db_amazonvatsalesdata(
     unique_account_identifier               string COMMENT '唯一帐户标识符'
    ,activity_period                         string COMMENT '活动期间'
    ,sales_channel                           string COMMENT '交易发货方式'
    ,marketplace                             string COMMENT '销售平台'
    ,program_type                            string COMMENT '项目类型'
    ,transaction_type                        string COMMENT '交易类型'
    ,transaction_event_id                    string COMMENT '交易ID'
    ,activity_transaction_id                 string COMMENT '事务ID'
    ,tax_calculation_date                    string COMMENT '计税日期'
    ,transaction_depart_date                 string COMMENT '交易发货日期'
    ,transaction_arrival_date                string COMMENT '到达日期'
    ,transaction_complete_date               string COMMENT '交易完成日期'
    ,seller_sku                              string COMMENT '卖家SKU'
    ,asin                                    string COMMENT '亚马逊产品编码'
    ,item_description                        string COMMENT '产品名称'
    ,item_manufacture_country                string COMMENT '产品制造国'
    ,qty                                     string COMMENT '下单数量'
    ,item_weight                             string COMMENT '重量'
    ,total_activity_weight                   string COMMENT '总重量'
    ,cost_price_of_items                     string COMMENT '成本'
    ,price_of_items_amt_vat_excl             string COMMENT '商品总价格不含增值税'
    ,promo_price_of_items_amt_vat_excl       string COMMENT '商品促销价格不含增值税'
    ,total_price_of_items_amt_vat_excl       string COMMENT '商品总价不含增值税'
    ,ship_charge_amt_vat_excl                string COMMENT '运费增值税不包括在内'
    ,promo_ship_charge_amt_vat_excl          string COMMENT '促销运费不含增值税'
    ,total_ship_charge_amt_vat_excl          string COMMENT '总运费增值税不包括在内'
    ,gift_wrap_amt_vat_excl                  string COMMENT '礼品包装费不含增值税'
    ,promo_gift_wrap_amt_vat_excl            string COMMENT '促销礼品包装费不含增值税'
    ,total_gift_wrap_amt_vat_excl            string COMMENT '礼品包装费合计不含增值税'
    ,total_activity_value_amt_vat_excl       string COMMENT '产品总金额不含增值税'
    ,price_of_items_vat_rate_percent         string COMMENT 'VAT税率'
    ,price_of_items_vat_amt                  string COMMENT '产品增值税金额'
    ,promo_price_of_items_vat_amt            string COMMENT '促销产品的增值税金额(优惠金额)'
    ,total_price_of_items_vat_amt            string COMMENT '产品增值税金额'
    ,ship_charge_vat_rate_percent            string COMMENT '运费增值税税率'
    ,ship_charge_vat_amt                     string COMMENT '运费增值税金额'
    ,promo_ship_charge_vat_amt               string COMMENT '促销运费增值税金额'
    ,total_ship_charge_vat_amt               string COMMENT '总运费增值税'
    ,gift_wrap_vat_rate_percent              string COMMENT '礼品包装费增值税税率'
    ,gift_wrap_vat_amt                       string COMMENT '礼品包装费增值税'
    ,promo_gift_wrap_vat_amt                 string COMMENT '促销礼品包装费增值税金额(优惠金额)'
    ,total_gift_wrap_vat_amt                 string COMMENT '礼品包装费增值税总额'
    ,total_activity_value_vat_amt            string COMMENT '订单总值增值税金额'
    ,price_of_items_amt_vat_incl             string COMMENT '商品价格(含增值税)'
    ,promo_price_of_items_amt_vat_incl       string COMMENT '产品优惠价格(含增值税)'
    ,total_price_of_items_amt_vat_incl       string COMMENT '商品总价(含增值税)'
    ,ship_charge_amt_vat_incl                string COMMENT '运费（含增值税)'
    ,promo_ship_charge_amt_vat_incl          string COMMENT '促销费用(含增值税)'
    ,total_ship_charge_amt_vat_incl          string COMMENT '总运费(含增值税)'
    ,gift_wrap_amt_vat_incl                  string COMMENT '礼品包装费(含增值税)'
    ,promo_gift_wrap_amt_vat_incl            string COMMENT '优惠包装费(含增值税)'
    ,total_gift_wrap_amt_vat_incl            string COMMENT '总包装费(含增值税)'
    ,total_activity_value_amt_vat_incl       string COMMENT '活动总销售额(含增值税）'
    ,transaction_currency_code               string COMMENT '交易币种'
    ,commodity_code                          string COMMENT '商品编码'
    ,statistical_code_depart                 string COMMENT '出发国代码'
    ,statistical_code_arrival                string COMMENT '到达国代码'
    ,commodity_code_supplementary_unit       string COMMENT '商品编码补充计量单位'
    ,item_qty_supplementary_unit             string COMMENT '商品数量补充计量单位'
    ,total_activity_supplementary_unit       string COMMENT '订单补充计量单位'
    ,product_tax_code                        string COMMENT '产品税务代码'
    ,depature_city                           string COMMENT '发运城市'
    ,departure_country                       string COMMENT '发运国家'
    ,departure_post_code                     string COMMENT '发运城市邮编'
    ,arrival_city                            string COMMENT '到达城市'
    ,arrival_country                         string COMMENT '到达国家'
    ,arrival_post_code                       string COMMENT '到达城市邮编'
    ,sale_depart_country                     string COMMENT '销售发运国家'
    ,sale_arrival_country                    string COMMENT '销售到达国家'
    ,transportation_mode                     string COMMENT '物流方式'
    ,delivery_conditions                     string COMMENT '交割模式'
    ,seller_depart_vat_number_country        string COMMENT '卖家发运地税号国家'
    ,seller_depart_country_vat_number        string COMMENT '卖家发运地税号'
    ,seller_arrival_vat_number_country       string COMMENT '卖家到达地税号国家'
    ,seller_arrival_country_vat_number       string COMMENT '卖家到达地税号'
    ,transaction_seller_vat_number_country   string COMMENT '交易卖方税号国家'
    ,transaction_seller_vat_number           string COMMENT '交易卖方税号'
    ,buyer_vat_number_country                string COMMENT '买家税号国家'
    ,buyer_vat_number                        string COMMENT '买家税号'
    ,vat_calculation_imputation_country      string COMMENT '增值税计算归算国'
    ,taxable_jurisdiction                    string COMMENT '税收管辖国家'
    ,taxable_jurisdiction_level              string COMMENT '税收管辖级别'
    ,vat_inv_number                          string COMMENT '联邦税号？'
    ,vat_inv_converted_amt                   string COMMENT '折算额'
    ,vat_inv_currency_code                   string COMMENT 'vat币种'
    ,vat_inv_exchange_rate                   string COMMENT '增值税兑换汇率'
    ,vat_inv_exchange_rate_date              string COMMENT '增值税汇率兑换日期'
    ,export_outside_eu                       string COMMENT '向欧盟以外地区出口'
    ,invoice_url                             string COMMENT '发票地址'
    ,buyer_name                              string COMMENT '买家姓名'
    ,arrival_address                         string COMMENT '收货地址'
    ,supplier_name                           string COMMENT '供应商名称'
    ,supplier_vat_number                     string COMMENT '供应商税号'
    ,tax_reporting_scheme                    string COMMENT '报税格式'
    ,tax_collection_responsibility           string COMMENT '税收征收责任方'
)
comment '亚马逊销售数据表'
partitioned by (ds string)
row format delimited fields terminated by ','
stored as Textfile
;