--let our N is 10, I use Standart SQL dialect, as for BigQuery

with bins as (
  select
    floor(metric_value / 10.0) * 10 as bin,
    count(user_id) as users
  from dataset.table
  group by 1
  order by 1
)

select
  bin,
  concat(bin,'-', bin + 10),
  users
from bins
order by 1
