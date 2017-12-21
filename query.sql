declare @t datetime, @s1 varchar(10), @s2 varchar(10)
set @s1 = 'SYM1'
set @s2 = 'SYM2'
set @t = 'DATE'

select @t = min(a.TradeDate)
from
(
select * from tblStockHistory
where Symbol = @s1 and TradeDate >= @t
) a
inner join
(
select * from tblStockHistory
where Symbol = @s2 and TradeDate >= @t
) b
on a.TradeDate = b.TradeDate

select a.TradeDate, 
a.[AdjClose]/a0.[AdjClose] 'SYM1', b.[AdjClose]/b0.[AdjClose] 'SYM2',
a.ImpliedVol252 IVF1, b.ImpliedVol252 IVF2
from
(
select * from tblStockHistory
where Symbol = @s1
) a
inner join
(
select * from tblStockHistory
where Symbol = @s2
) b
on a.TradeDate = b.TradeDate
cross join
(
select * from tblStockHistory
where Symbol = @s1 and TradeDate = @t
) a0
cross join
(
select * from tblStockHistory
where Symbol = @s2 and TradeDate = @t
) b0
where a.TradeDate >= @t
order by 1


