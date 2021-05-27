
--Frequency analysis on the 'myShelter' URL parameter
--Example: https://www.atweather.org/forecast?myState=MD&myShelter=134

WITH cte AS
(
SELECT CASE WHEN loc_id = '' THEN 0 ELSE CAST(loc_id AS integer) END AS loc_id, 
       COUNT(*) AS freq
FROM
(
	SELECT split_part(path, '=', 4) AS loc_id 
	FROM access_log 
	WHERE path SIMILAR TO '%myShelter=[0-9]*'
) a
GROUP BY loc_id
)

SELECT l.id, l.location, cte.freq
FROM locations l LEFT JOIN cte ON l.id = cte.loc_id
ORDER BY l.id;
