SELECT 
dps.department,
jb.names as job,
SUM(CASE WHEN QUARTER(hiremmp.datetimeshired) = 1 THEN 1 ELSE 0 END) AS Q1,
SUM(CASE WHEN QUARTER(hiremmp.datetimeshired) = 2 THEN 1 ELSE 0 END) AS Q2,
SUM(CASE WHEN QUARTER(hiremmp.datetimeshired) = 3 THEN 1 ELSE 0 END) AS Q3,
SUM(CASE WHEN QUARTER(hiremmp.datetimeshired) = 4 THEN 1 ELSE 0 END) AS Q4
FROM hired_employees hiremmp
INNER JOIN jobs jb ON hiremmp.job_id = jb.id
INNER JOIN departments dps ON hiremmp.departament_id = dps.id
WHERE YEAR(hiremmp.datetimeshired) = 2021
GROUP BY
dps.department,
jb.names 
ORDER BY dps.department,jb.names