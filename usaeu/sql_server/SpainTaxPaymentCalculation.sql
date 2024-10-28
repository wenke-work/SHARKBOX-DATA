/*
西班牙税务申报计算:
@Declare_Serial_Number : 流水号
*/
use vat_db
go
drop procedure if exists dbo.SpainTaxPaymentCalculation;
go
create procedure dbo.SpainTaxPaymentCalculation
     @Declare_Serial_Number varchar(100)
    ,@Declare_Date varchar(100)
as
begin
-- 判断是否有数据存在-交易当天找不到 外币兑 申报币种的 汇率 
declare @Result int
select @Result=COUNT(1) from dbo.VatView_AmazonVATSalesData
where Sale_Depart_Country='ES'
  and Declare_AMT_VAT_INCL=9999999999.99999999
  and Declare_Serial_Number=@Declare_Serial_Number
  and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
  and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0

if @Result > 0
begin
    return -1
end
;
-- 根据参数-流水号拿取数据
with DataListTmp as(
select
     Declare_Serial_Number                                         --业务流水号
    ,Declare_Currency                                              --申报币种
    ,Declare_AMT_VAT_INCL                                          --申报含税金额
    ,Tax_Collection_Responsibility                                 --CQ列-税收征收责任方
    ,Taxable_JurisdicTion                                          --CC列-税收管辖国家
    ,Transaction_Type                                              --F列-交易类型
    ,Price_Of_Items_Vat_Rate_Percent                               --AE列-VAT税率
    ,Buyer_Vat_Number                                              --CA列-买家税号
    ,Sale_Depart_Country                                           --BP列-销售发运国家
    ,Sale_Arrival_Country                                          --BQ列-销售到达国家
    ,iif(Sale_Depart_Country in('AT','BE','BG','CY','CZ','HR','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','RO','LT','LU','MT','NL','PL','PT','SK','SI','ES','SE'),'欧盟成员国','非欧盟成员国')    as StartEuropeanUnion         --发运国是否欧盟成员国
    ,iif(Sale_Arrival_Country in('AT','BE','BG','CY','CZ','HR','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','RO','LT','LU','MT','NL','PL','PT','SK','SI','ES','SE'),'欧盟成员国','非欧盟成员国')   as DestinationEuropeanUnion   --到达国是否欧盟成员国
    ,iif(Buyer_Vat_Number like '%ES%','Y','N')                                                                                                                                                           as IsES
from
    dbo.VatView_AmazonVATSalesData
where Declare_Serial_Number=@Declare_Serial_Number
  and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
  and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
)

-- 代扣代缴订单
, WithholdAndRemit as(
select
     Declare_Serial_Number
    ,Declare_Currency
    ,sum(Declare_AMT_VAT_INCL)                                                                                                                                                      as WithholdSaleAmount         --代扣代缴净销售额
from
    DataListTmp
where Tax_Collection_Responsibility='MARKETPLACE'
  and Taxable_JurisdicTion='SPAIN'
  and StartEuropeanUnion='欧盟成员国'
  and DestinationEuropeanUnion='欧盟成员国'
group by Declare_Serial_Number
        ,Declare_Currency
)

-- 自行缴费订单
, SelfPayment as(
select
     Declare_Serial_Number
    ,sum(iif(isnull(Price_Of_Items_Vat_Rate_Percent,0)<>0 and Buyer_Vat_Number is not null and Sale_Depart_Country='ES' and DestinationEuropeanUnion='欧盟成员国',Declare_AMT_VAT_INCL,0))                                              as SelfSpainToEuropean             --西班牙到欧盟(税率大于0)
    ,sum(iif(isnull(Price_Of_Items_Vat_Rate_Percent,0)<>0 and Buyer_Vat_Number is null and Sale_Arrival_Country='ES' and StartEuropeanUnion='欧盟成员国',Declare_AMT_VAT_INCL,0))                                                       as SelfEuropeanToSpain             --欧盟到西班牙(税率大于0)
    ,sum(iif(Price_Of_Items_Vat_Rate_Percent is null and Buyer_Vat_Number is null and Sale_Arrival_Country='ES' and StartEuropeanUnion='欧盟成员国',Declare_AMT_VAT_INCL,0))                                                            as SelfEuropeanToSpainVatNull      --欧盟到西班牙(税率空白)
    ,sum(iif(isnull(Price_Of_Items_Vat_Rate_Percent,0)=0 and Buyer_Vat_Number is not null and Sale_Depart_Country='ES' and DestinationEuropeanUnion='欧盟成员国' and Sale_Arrival_Country<>'ES' and IsES='N',Declare_AMT_VAT_INCL,0))   as CrossBorderB2BGrossSaleAmount   --跨境B2B净销售额
    ,sum(iif(isnull(Price_Of_Items_Vat_Rate_Percent,0)=0 and Buyer_Vat_Number is not null and Sale_Depart_Country='ES' and Sale_Arrival_Country='ES' and IsES='Y',Declare_AMT_VAT_INCL,0))                                              as DomesticB2BGrossSaleAmount      --本地B2B净销售额
from
    DataListTmp
where Transaction_Type<>'COMMINGLING_BUY'
  and Tax_Collection_Responsibility='SELLER'
group by Declare_Serial_Number
)

-- 共享库存购买(抵扣部分)
, DeductionAmount as(
select
     Declare_Serial_Number
    ,sum(Declare_AMT_VAT_INCL)                                      as ProcureAmount                 -- 采购金额
from
    DataListTmp
where Transaction_Type='COMMINGLING_BUY'
  and isnull(Price_Of_Items_Vat_Rate_Percent,0)=0
  and Buyer_Vat_Number is not null
  and StartEuropeanUnion='欧盟成员国'
  and Sale_Depart_Country<>'ES'
  and Sale_Arrival_Country='ES'
group by Declare_Serial_Number
)

-- 结果汇总
, ResultSetList as(
select
     tb0.Declare_Serial_Number
    ,tb1.Declare_Currency
    ,'amazon'                                                                                       as Platform
    ,'西班牙'                                                                                       as Country
    ,tb1.WithholdSaleAmount                                                                         as WithholdSaleAmount              -- 代扣代缴净销售额
    ,tb2.SelfSpainToEuropean + tb2.SelfEuropeanToSpain + tb2.SelfEuropeanToSpainVatNull             as SellerGrossSaleAmount           -- 自缴含税销售额(税率大于0和空白)
    ,0                                                                                              as SellerNetSaleAmountTaxRate0     -- 自缴净销售额(税率等于0)
    ,tb2.DomesticB2BGrossSaleAmount                                                                 as DomesticB2BNetSaleAmount        -- 本地B2B净销售额
    ,tb2.CrossBorderB2BGrossSaleAmount                                                              as CrossBorderB2BNetSaleAmount     -- 跨境B2B净销售额
    ,tb3.ProcureAmount                                                                              as ProcureAmount                   -- 采购金额
    ,0                                                                                              as PVATaxAmount                    -- 递延税额
    ,0                                                                                              as OtherDeductionsTaxAmount        -- 其它抵扣税额
    ,tb0.RateValue                                                                                  as GreaterZeroTaxRate              -- 大于0税率
    ,0                                                                                              as Interest                        -- 利息
from
    (select @Declare_Serial_Number as Declare_Serial_Number,RateValue from dbo.VAT_rate where CountryId in(select ID from dbo.Country where CountryName='西班牙')) tb0
left join
    WithholdAndRemit tb1
on tb0.Declare_Serial_Number=tb1.Declare_Serial_Number
left join
    SelfPayment tb2
on tb0.Declare_Serial_Number=tb2.Declare_Serial_Number
left join
    DeductionAmount tb3
on tb0.Declare_Serial_Number=tb3.Declare_Serial_Number
)

merge into dbo.Vat_AmazonTaxPaymentCalculation tb1
using ResultSetList tb2
on tb1.Declare_Serial_Number=tb2.Declare_Serial_Number and tb1.Country=tb2.Country
when matched
then update set tb1.WithholdSaleAmount=isnull(tb2.WithholdSaleAmount,0)
               ,tb1.SellerGrossSaleAmount=isnull(tb2.SellerGrossSaleAmount,0)
               ,tb1.SellerNetSaleAmountTaxRate0=isnull(tb2.SellerNetSaleAmountTaxRate0,0)
               ,tb1.DomesticB2BNetSaleAmount=isnull(tb2.DomesticB2BNetSaleAmount,0)
               ,tb1.CrossBorderB2BNetSaleAmount=isnull(tb2.CrossBorderB2BNetSaleAmount,0)
               ,tb1.ProcureAmount=isnull(tb2.ProcureAmount,0)
               ,tb1.GreaterZeroTaxRate=isnull(tb2.GreaterZeroTaxRate,0)
               ,tb1.Interest=isnull(tb2.Interest,0)
               ,tb1.ModifyDate=getdate()
when not matched
then insert values(tb2.Declare_Serial_Number
                  ,tb2.Declare_Currency
                  ,tb2.Platform
                  ,tb2.Country
                  ,isnull(tb2.WithholdSaleAmount,0)
                  ,isnull(tb2.SellerGrossSaleAmount,0)
                  ,isnull(tb2.SellerNetSaleAmountTaxRate0,0)
                  ,isnull(tb2.DomesticB2BNetSaleAmount,0)
                  ,isnull(tb2.CrossBorderB2BNetSaleAmount,0)
                  ,isnull(tb2.ProcureAmount,0)
                  ,tb2.PVATaxAmount
                  ,tb2.OtherDeductionsTaxAmount
                  ,isnull(tb2.GreaterZeroTaxRate,0)
                  ,isnull(tb2.Interest,0)
                  ,getdate()
                  ,getdate()
                  ,null                                               -- 自缴-德国到欧盟外
                  ,null                                               -- 自缴-德国到欧盟
                  ,null                                               -- 欧盟B2B采购销售额(如清关递延,不含税金额)
                  ,null                                               -- 欧盟服务发票销售额(如卢森堡发票，不含金额，一般指亚马逊开给b端的发票)
                  ,null                                               -- 税金
                  ,null                                               -- 最终缴纳税金(税金+利息)
                  ,null                                               -- 自缴净销售额(税率大于0和空白)
                  )
;
return 0
end
go