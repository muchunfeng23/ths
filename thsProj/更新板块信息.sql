truncate table share_plates;
insert into share_plates (share_code,plates)
select share_code,GROUP_CONCAT(plate_name) from crawler_share_plate_info group by share_code