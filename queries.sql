-- Analytical queries for the salon performance tracker
-- Demonstrates: JOINs, aggregate functions, GROUP BY, window functions, subqueries

-- 1. Average performance score by location, ranked
SELECT
    t.location,
    ROUND(AVG(m.final_score), 1) AS avg_score,
    COUNT(DISTINCT m.technician_id) AS technician_count
FROM monthly_performance m
JOIN technicians t ON t.technician_id = m.technician_id
GROUP BY t.location
ORDER BY avg_score DESC;

-- 2. Top 3 performers per month (window function)
SELECT month, name, location, final_score, tier
FROM (
    SELECT
        m.month,
        t.name,
        t.location,
        m.final_score,
        m.tier,
        RANK() OVER (PARTITION BY m.month ORDER BY m.final_score DESC) AS rnk
    FROM monthly_performance m
    JOIN technicians t ON t.technician_id = m.technician_id
) ranked
WHERE rnk <= 3
ORDER BY month, rnk;

-- 3. Technicians whose retention is consistently below the network average
SELECT t.name, t.location, ROUND(AVG(m.client_retention_pct), 1) AS avg_retention
FROM monthly_performance m
JOIN technicians t ON t.technician_id = m.technician_id
GROUP BY t.technician_id, t.name, t.location
HAVING AVG(m.client_retention_pct) < (
    SELECT AVG(client_retention_pct) FROM monthly_performance
)
ORDER BY avg_retention ASC;

-- 4. Month-over-month revenue change per location
SELECT
    location,
    month,
    revenue,
    revenue - LAG(revenue) OVER (PARTITION BY location ORDER BY month_order) AS revenue_change
FROM (
    SELECT
        t.location,
        m.month,
        SUM(m.revenue) AS revenue,
        CASE m.month
            WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3
            WHEN 'July' THEN 4 WHEN 'August' THEN 5
        END AS month_order
    FROM monthly_performance m
    JOIN technicians t ON t.technician_id = m.technician_id
    GROUP BY t.location, m.month
) location_revenue
ORDER BY location, month_order;

-- 5. Total bonus payout by tier and month
SELECT month, tier, COUNT(*) AS headcount, SUM(bonus_gbp) AS total_bonus
FROM monthly_performance
GROUP BY month, tier
ORDER BY month, total_bonus DESC;
