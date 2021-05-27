
--Pull last 2500 records for requests that specify the 'myShelter' URL parameter
--This simple formulation relies on the parameter being at the end of the URL

--Example: https://www.atweather.org/forecast?myState=MD&myShelter=134

SELECT *
FROM access_log 
WHERE path SIMILAR TO '%myShelter=[0-9]*'
ORDER BY local_time DESC
LIMIT 2500;