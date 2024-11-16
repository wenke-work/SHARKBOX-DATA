-- 采购订单_采购单
drop procedure if exists sharkbox_merge.proc_lingxing_purchase_product;
DELIMITER //
CREATE PROCEDURE sharkbox_merge.proc_lingxing_purchase_product()
BEGIN
UPDATE sharkbox_merge.lingxing_purchase_product tb1
LEFT JOIN
    sharkbox_merge.lingxing_warehouse_owner tb2
ON tb1.purchase_warehouse=tb2.lingxing_warehouse
LEFT JOIN
    (SELECT purchase_number,batch_number,COUNT(1) AS cn FROM sharkbox_merge.lingxing_purchase_product GROUP BY purchase_number,batch_number) tb3
ON tb1.purchase_number=tb3.purchase_number
SET tb1.data_owner=tb2.we_owner_code
   ,tb1.data_number=tb3.cn
;
END //
DELIMITER ;

-- 加工计划_采购-单品明细
drop procedure if exists sharkbox_merge.proc_lingxing_purchase_processing_plan;
DELIMITER //
CREATE PROCEDURE sharkbox_merge.proc_lingxing_purchase_processing_plan()
BEGIN
UPDATE sharkbox_merge.lingxing_purchase_processing_plan tb1
LEFT JOIN
    sharkbox_merge.lingxing_warehouse_owner tb2
ON tb1.warehouse=tb2.lingxing_warehouse
LEFT JOIN
    (SELECT processing_plan_number,batch_number,COUNT(1) AS cn FROM sharkbox_merge.lingxing_purchase_processing_plan GROUP BY processing_plan_number,batch_number) tb3
ON tb1.processing_plan_number=tb3.processing_plan_number
SET tb1.data_owner=tb2.we_owner_code
   ,tb1.data_number=tb3.cn
;
END //
DELIMITER ;