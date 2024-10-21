-- VAT申报-各国申报税务计算结果表
use vat_db
go
drop table if exists dbo.Vat_AmazonTaxPaymentCalculation;
create table dbo.Vat_AmazonTaxPaymentCalculation(
     ID int identity(1,1) primary key
    ,Declare_Serial_Number varchar(100)
    ,Declare_Currency varchar(100)
    ,Platform varchar(100)
    ,Country varchar(100)
    ,WithholdSaleAmount decimal(38,8)
    ,SellerGrossSaleAmount decimal(38,8)
    ,SellerNetSaleAmountTaxRate0 decimal(38,8)
    ,DomesticB2BNetSaleAmount decimal(38,8)
    ,CrossBorderB2BNetSaleAmount decimal(38,8)
    ,ProcureAmount decimal(38,8)
    ,PVATaxAmount decimal(38,8)
    ,OtherDeductionsTaxAmount decimal(38,8)
    ,GreaterZeroTaxRate decimal(38,8)
    ,Interest decimal(38,8)
    ,CreateDate datetime default getdate()
    ,ModifyDate datetime default getdate()
    ,DE_SelfGermanyToNotEuropean decimal(38,8)
    ,DE_SelfGermanyToEuropean decimal(38,8)
)
-- 表加注释
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'VAT申报-各国申报税务计算结果表' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation'
GO
-- 字段加注释
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'主键' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'ID'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'业务流水号' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'Declare_Serial_Number'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'申报币种' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'Declare_Currency'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'平台' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'Platform'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'国家' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'Country'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'代扣代缴净销售额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'WithholdSaleAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'自缴含税销售额(税率大于0和空白)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'SellerGrossSaleAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'自缴净销售额(税率等于0)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'SellerNetSaleAmountTaxRate0'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'本地B2B净销售额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'DomesticB2BNetSaleAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'跨境B2B净销售额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'CrossBorderB2BNetSaleAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'采购金额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'ProcureAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'递延税额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'PVATaxAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'其它抵扣税额' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'OtherDeductionsTaxAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'大于0税率' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'GreaterZeroTaxRate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'利息' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'Interest'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'创建时间' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'CreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'修改时间' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'ModifyDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'自缴-德国到欧盟外' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'DE_SelfGermanyToNotEuropean'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'自缴-德国到欧盟' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'DE_SelfGermanyToEuropean'
GO
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- vat_税务申报查询视图
use vat_db
go
drop view if exists VatView_AmazonTaxPaymentCalculation;
go
create view VatView_AmazonTaxPaymentCalculation as
select
     Declare_Serial_Number                                                                                                                                                 --业务流水号
    ,Declare_Currency                                                                                                                                                      --申报币种
    ,WithholdSaleAmount                                                                                                                                                    --代扣代缴净销售额
    ,SellerGrossSaleAmount + (SellerNetSaleAmountTaxRate0 * (1 + GreaterZeroTaxRate))                               as SellerTotalGrossSaleAmount                          --自缴含税总销售额
    ,SellerNetSaleAmount                                                                                                                                                   --自缴净销售额
    ,SellerNetSaleAmount + WithholdSaleAmount                                                                       as TotalNetSaleAmount                                  --全部净销售额(自缴净销售额+代扣代缴金额)
    ,SalePVATaxAmount                                                                                                                                                      --销项税
    ,iif(GreaterZeroTaxRate<>0,SalePVATaxAmount/GreaterZeroTaxRate,0)                                               as NetSaleAmount                                       --销项不含税金额
    ,iif(GreaterZeroTaxRate<>0,(ProcureTaxAmount + OtherDeductionsTaxAmount + PVATaxAmount)/GreaterZeroTaxRate,0)   as NetProcureAmount                                    --进项不含税金额
    ,ProcureTaxAmount + OtherDeductionsTaxAmount + PVATaxAmount                                                     as ProcurePVATaxAmount                                 --进项税
    ,PVATaxAmount                                                                                                                                                          --递延税金
    ,ProcureTaxAmount                                                                                                                                                      --采购抵扣税金
    ,OtherDeductionsTaxAmount                                                                                                                                              --其他项抵扣税金
    ,Interest                                                                                                                                                              --利息税金
    ,SalePVATaxAmount - (ProcureTaxAmount + OtherDeductionsTaxAmount + PVATaxAmount ) + Interest                    as FinalTaxAmount                                      --最终应纳税金
    ,DomesticB2BNetSaleAmount                                                                                                                                              --本地B2B净销售额
    ,CrossBorderB2BNetSaleAmount                                                                                                                                           --跨境B2B净销售额
    ,ALLB2BNetSaleAmount                                                                                                                                                   --全部B2B净销售额
    ,GreaterZeroTaxRate                                                                                                                                                    --标准税率
    ,SellerNetSaleAmountTaxRateGreater0                                                                                                                                    --自缴净销售额(税率大于0和空白)
    ,SellerNetSaleAmountTaxRate0                                                                                                                                           --自缴净销售额(税率等于0)
    ,CreateDate                                                                                                                                                            --创建时间
    ,ModifyDate                                                                                                                                                            --修改时间
    ,DE_SelfGermanyToNotEuropean                                                                                                                                           --自缴-德国到欧盟外
    ,DE_SelfGermanyToEuropean                                                                                                                                              --自缴-德国到欧盟
    ,EUB2BPurchaseSaleAmount                                                                                                                                               --欧盟B2B采购销售额(如清关递延,不含税金额)
    ,EUInvoiceSaleAmount                                                                                                                                                   --欧盟服务发票销售额(如卢森堡发票，不含金额，一般指亚马逊开给b端的发票)
from
    (
        select
             ID                                                                                                                                                            --主键
            ,Declare_Serial_Number                                                                                                                                         --业务流水号
            ,Declare_Currency                                                                                                                                              --申报币种
            ,Platform                                                                                                                                                      --平台
            ,Country                                                                                                                                                       --国家
            ,WithholdSaleAmount                                                                                                                                            --代扣代缴净销售额
            ,SellerGrossSaleAmount                                                                                                                                         --自缴含税销售额(税率大于0和空白)
            ,SellerNetSaleAmountTaxRate0                                                                                                                                   --自缴净销售额(税率等于0)
            ,DomesticB2BNetSaleAmount                                                                                                                                      --本地B2B净销售额
            ,CrossBorderB2BNetSaleAmount                                                                                                                                   --跨境B2B净销售额
            ,DomesticB2BNetSaleAmount + CrossBorderB2BNetSaleAmount                                                                as ALLB2BNetSaleAmount                  --全部B2B净销售额
            ,ProcureAmount                                                                                                                                                 --采购金额
            ,PVATaxAmount                                                                                                                                                  --递延税额
            ,OtherDeductionsTaxAmount                                                                                                                                      --其它抵扣税额
            ,GreaterZeroTaxRate                                                                                                                                            --大于0税率
            ,Interest                                                                                                                                                      --利息
            ,CreateDate                                                                                                                                                    --创建时间
            ,ModifyDate                                                                                                                                                    --修改时间
            ,DE_SelfGermanyToNotEuropean                                                                                                                                   --自缴-德国到欧盟外
            ,DE_SelfGermanyToEuropean                                                                                                                                      --自缴-德国到欧盟
            ,EUB2BPurchaseSaleAmount                                                                                                                                       --欧盟B2B采购销售额(如清关递延,不含税金额)
            ,EUInvoiceSaleAmount                                                                                                                                           --欧盟服务发票销售额(如卢森堡发票，不含金额，一般指亚马逊开给b端的发票)
            ,SellerGrossSaleAmount /(1 + GreaterZeroTaxRate)                                                                       as SellerNetSaleAmountTaxRateGreater0   --自缴净销售额(税率大于0和空白)
            ,SellerGrossSaleAmount /(1 + GreaterZeroTaxRate) + SellerNetSaleAmountTaxRate0                                         as SellerNetSaleAmount                  --自缴净销售额(税率大于0和空白+税率等于0)
            ,(SellerGrossSaleAmount /(1 + GreaterZeroTaxRate) + SellerNetSaleAmountTaxRate0) * GreaterZeroTaxRate + PVATaxAmount   as SalePVATaxAmount                     --销项税
            ,ProcureAmount/(1 + GreaterZeroTaxRate) * GreaterZeroTaxRate                                                           as ProcureTaxAmount                     --采购抵扣税金
        from
            dbo.Vat_AmazonTaxPaymentCalculation
    ) tmp
go

EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'vat_税务申报查询', @level0type = N'SCHEMA', @level0name = 'dbo', @level1type = N'VIEW', @level1name = 'VatView_AmazonTaxPaymentCalculation';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'业务流水号',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'Declare_Serial_Number';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'申报币种',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'Declare_Currency';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'代扣代缴净销售额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'WithholdSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴含税总销售额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'SellerTotalGrossSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴净销售额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'SellerNetSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'全部净销售额(自缴净销售额+代扣代缴金额)',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'TotalNetSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'销项税',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'SalePVATaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'销项不含税金额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'NetSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'进项不含税金额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'NetProcureAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'进项税',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'ProcurePVATaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'递延税金',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'PVATaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'采购抵扣税金',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'ProcureTaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'其他项抵扣税金',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'OtherDeductionsTaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'利息税金',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'Interest';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'最终应纳税金',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'FinalTaxAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'本地B2B净销售额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'DomesticB2BNetSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'跨境B2B净销售额',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'CrossBorderB2BNetSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'标准税率',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'GreaterZeroTaxRate';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴净销售额(税率大于0和空白)',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'SellerNetSaleAmountTaxRateGreater0';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴净销售额(税率等于0)',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'SellerNetSaleAmountTaxRate0';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'创建时间',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'CreateDate';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'修改时间',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'ModifyDate';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴-德国到欧盟外',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'DE_SelfGermanyToNotEuropean';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'自缴-德国到欧盟',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'DE_SelfGermanyToEuropean';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'欧盟B2B采购销售额(如清关递延,不含税金额)',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'EUB2BPurchaseSaleAmount';
go
EXEC sp_addextendedproperty @name = N'MS_Description',@value = N'欧盟服务发票销售额(如卢森堡发票，不含金额，一般指亚马逊开给b端的发票)',@level0type = N'Schema', @level0name = 'dbo',@level1type = N'View',  @level1name = 'VatView_AmazonTaxPaymentCalculation',@level2type = N'Column', @level2name = 'EUInvoiceSaleAmount';
go
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- vat视图_亚马逊销售数据
use vat_db
go
drop view if exists VatView_AmazonVATSalesData;
go
create view VatView_AmazonVATSalesData
as
select *
from
    (
        select
             tb1.Declare_Serial_Number                                                                                                                                         -- 业务流水号
            ,case when tb1.Transaction_Currency_Code=tb1.ReportingCurrencyCode                                                                                          then tb1.Total_Activity_Value_Amt_Vat_Incl
                  when tb2.TargetCurrencyCode is not null                                                                                                               then tb1.Total_Activity_Value_Amt_Vat_Incl / tb2.RateValue
                  when tb1.Transaction_Currency_Code <> tb1.ReportingCurrencyCode and tb2.TargetCurrencyCode is null and isnull(tb1.Transaction_Currency_Code,'')<>''   then 9999999999.99999999
                  else 0
             end                                                                                                                            as Declare_AMT_VAT_INCL            -- 申报含税金额
            ,tb1.ReportingCurrencyCode                                                                                                      as Declare_Currency                -- 申报币种
            ,tb2.RateValue                                                                                                                  as Declare_Currency_Rate           -- 当月汇率
            ,tb1.Price_Of_Items_Vat_Rate_Percent                                                                                            as Declare_VAT_Rate                -- 申报税率
            ,tb1.Total_Activity_Value_Amt_Vat_Incl / (1 + tb1.Price_Of_Items_Vat_Rate_Percent)                                              as Declare_AMT_VAT_EXCL            -- 申报不含税金额
            ,tb1.Total_Activity_Value_Amt_Vat_Incl / (1 + tb1.Price_Of_Items_Vat_Rate_Percent) * tb1.Price_Of_Items_Vat_Rate_Percent        as Declare_Tax                     -- 申报税额
            ,tb1.Tax_Collection_Responsibility                                                                                                                                 -- CQ列-税收征收责任方
            ,tb1.Taxable_JurisdicTion                                                                                                                                          -- CC列-税收管辖国家
            ,tb1.Transaction_Type                                                                                                                                              -- F列-交易类型
            ,tb1.Price_Of_Items_Vat_Rate_Percent                                                                                                                               -- AE列-VAT税率
            ,tb1.Buyer_Vat_Number                                                                                                                                              -- CA列-买家税号
            ,tb1.Sale_Depart_Country                                                                                                                                           -- BP列-销售发运国家
            ,tb1.Sale_Arrival_Country                                                                                                                                          -- BQ列-销售到达国家
            ,tb1.TransacTion_Event_Id                                                                                                                                          -- 交易ID
            ,tb1.Transaction_Currency_Code                                                                                                                                     -- BB列-交易币种
            ,tb1.TransacTion_Complete_Date                                                                                                                                     -- L列-交易完成日期
            ,tb1.CountryTwoCode                                                                                                                                                -- 申报国家二字码
            ,tb1.ID                                                                                                                                                            -- 主键
            ,row_number() over(partition by tb1.ID order by tb2.ModificationDate desc)                                                      as st                              -- 排序
        FROM
            (
                select
                     t1.ID                                                                                                                                                     -- 主键
                    ,t1.Declare_Serial_Number                                                                                                                                  -- 业务流水号
                    ,t1.Tax_Collection_Responsibility                                                                                                                          -- CQ列-税收征收责任方
                    ,t1.Taxable_JurisdicTion                                                                                                                                   -- CC列-税收管辖国家
                    ,t1.Transaction_Type                                                                                                                                       -- F列-交易类型
                    ,t1.Price_Of_Items_Vat_Rate_Percent                                                                                                                        -- AE列-VAT税率
                    ,t1.Buyer_Vat_Number                                                                                                                                       -- CA列-买家税号
                    ,t1.Sale_Depart_Country                                                                                                                                    -- BP列-销 售发运国家
                    ,t1.Sale_Arrival_Country                                                                                                                                   -- BQ列-销售到达国家
                    ,t1.Total_Activity_Value_Amt_Vat_Incl                                                                                                                      -- BA列-活动总销售额(含增值税）
                    ,t1.TransacTion_Event_Id                                                                                                                                   -- 交易ID
                    ,t1.Transaction_Currency_Code                                                                                                                              -- BB列-交易币种
                    ,t1.TransacTion_Complete_Date                                                                                                                              -- L列-交易完成日期
                    ,t1.CountryTwoCode                                                                                                                                         -- 申报国家二字码
                    ,t2.ReportingCurrencyCode                                                                                                                                  -- 申报货币-三字代码
                from
                    dbo.AmazonVATSalesData t1
                left join
                    (
                        select
                             table1.CountryTwoCode                                                                                                                             -- 国家二字代码
                            ,table2.CurrencyThreeCode   as ReportingCurrencyCode                                                                                               -- 申报货币-三字代码
                        from
                            (
                                select
                                     CountryTwoCode                                                                                                                            -- 国家二字代码
                                    ,ReportingCurrencyId                                                                                                                       -- 申报货币id
                                    ,row_number() over(partition by CountryTwoCode order by isnull(ModificationDate,CreationDate) desc)   as st
                                from
                                    dbo.Country                                                                                                                                -- 国家表
                            ) table1
                        left join
                            (select ID,CurrencyThreeCode from dbo.Currency) table2                                                                                             -- 币种表
                        on table1.ReportingCurrencyId=table2.ID
                        where st=1
                    ) t2
                on t1.CountryTwoCode = t2.CountryTwoCode
            ) tb1
        left join
            (
                select
                     t1.BaseCountryTwoCode                                                                                                                                     -- 本币国家二字代码 预留字段
                    ,t1.BaseCurrencyId                                                                                                                                         -- 本国货币id
                    ,t1.TargetCurrencyId                                                                                                                                       -- 目标货币id
                    ,t2.CurrencyThreeCode                                   as BaseCurrencyCode                                                                                -- 本国货币-三字代码
                    ,t3.CurrencyThreeCode                                   as TargetCurrencyCode                                                                              -- 目标货币-三字代码
                    ,t1.RateValue                                                                                                                                              -- 汇率
                    ,t1.EffectiveDateStart                                                                                                                                     -- 汇率有效日期——开始
                    ,t1.EffectiveDateEnd                                                                                                                                       -- 汇率有效日期——结束
                    ,t1.ModificationDate                                                                                                                                       -- 最后修改时间
                from
                    dbo.ExchangeRate t1
                left join
                    (select ID,CurrencyThreeCode from dbo.Currency) t2                                                                                                         -- 币种表 tb2
                on t1.BaseCurrencyId=t2.ID
                left join
                    (select ID,CurrencyThreeCode from dbo.Currency) t3                                                                                                         -- 币种表 tb2
                on t1.TargetCurrencyId=t3.ID
            ) tb2
        on tb1.ReportingCurrencyCode = tb2.BaseCurrencyCode
        and tb1.Transaction_Currency_Code = tb2.TargetCurrencyCode
        and tb1.TransacTion_Complete_Date >= tb2.EffectiveDateStart
        and tb1.TransacTion_Complete_Date <= tb2.EffectiveDateEnd
    ) tmp
where st=1
go
EXEC sp_addextendedproperty @name = N'MS_Description', @value = N'vat视图_亚马逊销售数据', @level0type = N'SCHEMA', @level0name = 'dbo', @level1type = N'VIEW', @level1name = 'VatView_AmazonVATSalesData';
go

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- 添加2024-10-16给计算结果表添加2个字段
use vat_db
go
alter table dbo.Vat_AmazonTaxPaymentCalculation add EUB2BPurchaseSaleAmount decimal(38,8) default 0
go
alter table dbo.Vat_AmazonTaxPaymentCalculation add EUInvoiceSaleAmount decimal(38,8) default 0
go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'欧盟B2B采购销售额(如清关递延,不含税金额)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'EUB2BPurchaseSaleAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'欧盟服务发票销售额(如卢森堡发票，不含金额，一般指亚马逊开给b端的发票)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'EUInvoiceSaleAmount'
GO

alter table dbo.Vat_AmazonTaxPaymentCalculation add TaxAmount decimal(38,8) default 0
go
alter table dbo.Vat_AmazonTaxPaymentCalculation add FinalTaxAmount decimal(38,8) default 0
go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'税金' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'TaxAmount'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'最终缴纳税金(税金+利息)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'FinalTaxAmount'
GO

alter table dbo.Vat_AmazonTaxPaymentCalculation add SellerNetSaleAmountTaxRateGreater0 decimal(38,8) default 0
go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'自缴净销售额(税率大于0和空白)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Vat_AmazonTaxPaymentCalculation', @level2type=N'COLUMN',@level2name=N'SellerNetSaleAmountTaxRateGreater0'
GO


