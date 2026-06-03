-- Query 1: Data Integrity & Health Check
SELECT 'dim_calendar' AS table_name, COUNT(*) AS row_count FROM dim_calendar
UNION ALL
SELECT 'dim_sell_prices' AS table_name, COUNT(*) AS row_count FROM dim_sell_prices
UNION ALL
SELECT 'fact_sales' AS table_name, COUNT(*) AS row_count FROM fact_sales;

-- Query 2: Top Selling Products (ABC Analysis Foundation)
SELECT 
    item_id, 
    SUM(sales) AS total_units_sold
FROM fact_sales
GROUP BY item_id
ORDER BY total_units_sold DESC
LIMIT 10;