
--Frequency analysis for common bots hitting the site's primary paths

WITH cte AS
(
SELECT bot_name
FROM ( VALUES ('Facebot'), 
              ('Petalbot'), 
			  ('PetalBot'), 
			  ('bingbot'), 
			  ('Ahrefsbot'), 
			  ('Adsbot'), 
			  ('facebookexternalhit'), 
			  ('woorank'), 
			  ('Sogou'), 
			  ('360Spider'), 
                          ('Googlebot'), 
			  ('semrush'), 
			  ('dotbot'), 
			  ('applebot'), 
			  ('smtbot'), 
			  ('MauiBot') )  bot(bot_name)
),

ua AS
(
SELECT cte.bot_name, a.*
FROM access_log a 
     LEFT JOIN cte ON a.user_agent LIKE CONCAT('%', cte.bot_name, '%')
WHERE (path = '/' OR path LIKE '/forecast%'
				  OR path LIKE '/learn%'
				  OR path LIKE '/about%')
)

SELECT bot_name, COUNT(*) AS frequency
FROM ua
GROUP BY bot_name
ORDER BY COUNT(*) DESC;
