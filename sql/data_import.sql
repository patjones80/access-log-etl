
psql -h at-weather.cybzabq6b2ft.us-west-2.rds.amazonaws.com -p 5432 -d access_log_main -U postgres -W
\COPY locations FROM '/home/jonesp/coding/atwx access-log/at_locations.txt' WITH DELIMITER '|';
