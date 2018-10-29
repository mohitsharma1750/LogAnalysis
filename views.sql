create view error_percent_log_view 
  as select date(time),round(100.0*sum(case log.status when '200 OK' 
  then 0 else 1 end)/count(log.status),2) as "error_percent" from log group by date(time) 
  order by "error_percent" desc;