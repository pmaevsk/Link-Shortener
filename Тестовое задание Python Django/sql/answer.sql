-- Task 1
SELECT b.client_number, 
       SUM(CASE WHEN ev.outcome='win' THEN 1 ELSE 0 END) AS 'Побед',
       SUM(CASE WHEN ev.outcome='lose' THEN 1 ELSE 0 END) AS 'Поражений'
FROM bid b INNER JOIN 
       event_value ev ON b.play_id=ev.play_id AND b.coefficient=ev.value
GROUP BY b.client_number;
-- Task 2
SELECT CONCAT(query.first_team, ' - ', query.second_team) AS game, 
       query.games AS games_count
FROM (SELECT LEAST(home_team, away_team) AS first_team, 
             GREATEST(home_team, away_team) AS second_team, 
             COUNT(*) AS games
FROM event_entity
GROUP BY first_team, second_team HAVING COUNT(*) >= 1
ORDER BY games) query;