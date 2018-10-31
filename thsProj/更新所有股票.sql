insert into all_shares (share_code,share_name)
select share_code,share_name from crawler_share_everyday_data where datekey = 20181031
group by share_code,share_name