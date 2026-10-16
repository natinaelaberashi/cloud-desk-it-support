-- SQLite-compatible portfolio analysis.
-- Import data/incidents.csv into a table named incidents using your SQLite client.
-- resolution_hours is treated as observed elapsed hours; averages use resolved cases only.

-- 1. Executive KPIs
SELECT COUNT(*) AS total_tickets,
       SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) AS resolved_tickets,
       SUM(CASE WHEN status IN ('Open','Pending') THEN 1 ELSE 0 END) AS backlog,
       ROUND(AVG(CASE WHEN status = 'Resolved' THEN resolution_hours END), 2) AS avg_resolved_hours,
       ROUND(100.0 * SUM(CASE WHEN status = 'Resolved' AND LOWER(sla_met) = 'true' THEN 1 ELSE 0 END)
         / NULLIF(SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END), 0), 2) AS resolved_sla_pct
FROM incidents;

-- 2. Backlog concentration by support team
SELECT team, COUNT(*) AS backlog_count
FROM incidents
WHERE status IN ('Open', 'Pending')
GROUP BY team
ORDER BY backlog_count DESC, team;

-- 3. Resolution time by priority
SELECT priority, COUNT(*) AS resolved_count,
       ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
WHERE status = 'Resolved'
GROUP BY priority
ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2
                       WHEN 'Medium' THEN 3 ELSE 4 END;

-- 4. Resolved SLA performance by team
SELECT team, COUNT(*) AS resolved_count,
       ROUND(100.0 * SUM(CASE WHEN LOWER(sla_met) = 'true' THEN 1 ELSE 0 END)
         / NULLIF(COUNT(*), 0), 2) AS sla_pct
FROM incidents
WHERE status = 'Resolved'
GROUP BY team
ORDER BY sla_pct ASC, team;
