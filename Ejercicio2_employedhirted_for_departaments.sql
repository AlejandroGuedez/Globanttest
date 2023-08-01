SELECT 
dps.id as departament_id,
department,
count(hiremmp.id) as hired
FROM hired_employees hiremmp
INNER JOIN departments dps ON hiremmp.departament_id = dps.id
WHERE YEAR(hiremmp.datetimeshired) = 2021
GROUP BY
dps.id,
department
ORDER BY count(hiremmp.id) desc