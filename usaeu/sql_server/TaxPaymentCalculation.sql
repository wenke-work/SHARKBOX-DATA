/*
用于税务申报计算，根据调用方提供的申报国家来执行该国家计算税款的存储过程，流水号和申报时间区间用于确定参与计算的具体数据集:
参数：
1.@Country ：申报国家
2.@DeclareSerialNumber ：流水号
3.@Declare_Date : 申报时间区间,格式-->2023-12-01to2024-02-29
返回值:
1.程序执行时会判断是否有数据存在交易当天找不到 外币兑 申报币种的 汇率的情况,有则中断执行 返回 外币code,用逗号分隔,无则正常执行,返回true
*/
use vat_db
go
drop procedure if exists dbo.TaxPaymentCalculation;
go

create procedure dbo.TaxPaymentCalculation
     @Country varchar(100)
    ,@Declare_Serial_Number varchar(100)
    ,@Declare_Date varchar(100)
    ,@Result varchar(300) output
as
begin
    declare @Status varchar(100)
    if @Country = '英国'
        begin
        execute @Status = BritainTaxPaymentCalculation @Declare_Serial_Number,@Declare_Date
        if @Status = 0
            begin
            select @Result='true'
            end
        else
            begin
            select @Result=string_agg(Transaction_Currency_Code,',')
            from
                (
                    select distinct Transaction_Currency_Code
                    from
                        dbo.VatView_AmazonVATSalesData
                    where CountryTwoCode='GB'
                      and Declare_AMT_VAT_INCL=9999999999.99999999
                      and Declare_Serial_Number=@Declare_Serial_Number
                      and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
                      and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
                ) tmp
            end
        end
    else if @Country = '德国'
        begin
        execute @Status = GermanyTaxPaymentCalculation @Declare_Serial_Number,@Declare_Date
        if @Status = 0
            begin
            select @Result='true'
            end
        else
            begin
            select @Result=string_agg(Transaction_Currency_Code,',')
            from
                (
                    select distinct Transaction_Currency_Code
                    from
                        dbo.VatView_AmazonVATSalesData
                    where CountryTwoCode='DE'
                      and Declare_AMT_VAT_INCL=9999999999.99999999
                      and Declare_Serial_Number=@Declare_Serial_Number
                      and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
                      and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
                ) tmp
            end
        end
    else if @Country = '法国'
        begin
        execute @Status = FranceTaxPaymentCalculation @Declare_Serial_Number,@Declare_Date
        if @Status = 0
            begin
            select @Result='true'
            end
        else
            begin
            select @Result=string_agg(Transaction_Currency_Code,',')
            from
                (
                    select distinct Transaction_Currency_Code
                    from
                        dbo.VatView_AmazonVATSalesData
                    where CountryTwoCode='FR'
                      and Declare_AMT_VAT_INCL=9999999999.99999999
                      and Declare_Serial_Number=@Declare_Serial_Number
                      and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
                      and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
                ) tmp
            end
        end
    else if @Country = '西班牙'
        begin
        execute @Status = SpainTaxPaymentCalculation @Declare_Serial_Number,@Declare_Date
        if @Status = 0
            begin
            select @Result='true'
            end
        else
            begin
            select @Result=string_agg(Transaction_Currency_Code,',')
            from
                (
                    select distinct Transaction_Currency_Code
                    from
                        dbo.VatView_AmazonVATSalesData
                    where CountryTwoCode='ES'
                      and Declare_AMT_VAT_INCL=9999999999.99999999
                      and Declare_Serial_Number=@Declare_Serial_Number
                      and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
                      and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
                ) tmp
            end
        end
    else if @Country = '意大利'
        begin
        execute @Status = ItalyTaxPaymentCalculation @Declare_Serial_Number,@Declare_Date
        if @Status = 0
            begin
            select @Result='true'
            end
        else
            begin
            select @Result=string_agg(Transaction_Currency_Code,',')
            from
                (
                    select distinct Transaction_Currency_Code
                    from
                        dbo.VatView_AmazonVATSalesData
                    where CountryTwoCode='IT'
                      and Declare_AMT_VAT_INCL=9999999999.99999999
                      and Declare_Serial_Number=@Declare_Serial_Number
                      and datediff(day,left(@Declare_Date,10),TransacTion_Complete_Date)>=0
                      and datediff(day,TransacTion_Complete_Date,right(@Declare_Date,10))>=0
                ) tmp
            end
        end
    else
        begin
            select @Result=concat('不支持这个国家：',@Country)
        end
end
go