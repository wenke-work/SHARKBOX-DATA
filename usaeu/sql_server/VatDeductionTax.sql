/*
税务抵扣项申报计算:
@Declare_Serial_Number : 流水号
*/
use vat_db
go
drop procedure if exists dbo.VatDeductionTax;
go
create procedure dbo.VatDeductionTax
@Declare_Serial_Number varchar(100)
as
begin
-- 根据参数-流水号拿取数据
with DataListTmp as(
select distinct
      tb1.DeclareSerialNumber                   as Declare_Serial_Number      --业务流水号
     ,tb1.DeadlineForTaxPayment                                               --截止缴税日期
     ,isnull(tb2.OtherDeductionsTaxAmount,0)    as OtherDeductionsTaxAmount   --其它抵扣税额
     ,isnull(tb3.PVATaxAmount,0)                as PVATaxAmount               --递延税额
from
    (select DeclareSerialNumber,Id,DeadlineForTaxPayment from dbo.VTADeclare where DeclareSerialNumber=@Declare_Serial_Number) tb1              --VTA申报表
left join
    (select VTADeclareId,isnull(sum(DeductionTax),0) as OtherDeductionsTaxAmount from dbo.AddOtherDeclarationItems group by VTADeclareId) tb2   --抵扣项表
on tb1.Id=tb2.VTADeclareId
left join
    (select VTADeclareId,isnull(sum(DeductionTax),0) as PVATaxAmount from dbo.AddOtherDeclarationItems2 group by VTADeclareId) tb3              --递延项表
on tb1.Id=tb3.VTADeclareId
)

update tb1 set tb1.PVATaxAmount=tb2.PVATaxAmount
          ,tb1.OtherDeductionsTaxAmount=tb2.OtherDeductionsTaxAmount
          ,tb1.ModifyDate=getdate()
          ,tb1.Interest=iif(tb1.Country='意大利' and datediff(day,getdate(),tb2.DeadlineForTaxPayment)<0,(tb1.SellerGrossSaleAmount/(1 + tb1.GreaterZeroTaxRate) * tb1.GreaterZeroTaxRate - (tb1.ProcureAmount/(1 + tb1.GreaterZeroTaxRate) * tb1.GreaterZeroTaxRate + tb2.OtherDeductionsTaxAmount)) * 0.01,0)
from
    dbo.Vat_AmazonTaxPaymentCalculation tb1
inner join
    DataListTmp tb2
on tb1.Declare_Serial_Number=tb2.Declare_Serial_Number
;
end
go