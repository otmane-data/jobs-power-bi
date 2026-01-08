
  
    
    

    create  table
      "duckdb"."main_gold"."dim_time__dbt_tmp"
  
    as (
      -- models/gold/dim_time.sql
-- Gold layer: Dimension Time



-- Generate a date dimension for time-based analysis
WITH date_spine AS (
    SELECT
        published_date,
        EXTRACT(YEAR FROM published_date) as year,
        EXTRACT(MONTH FROM published_date) as month,
        EXTRACT(QUARTER FROM published_date) as quarter,
        EXTRACT(WEEK FROM published_date) as week,
        EXTRACT(DAYOFWEEK FROM published_date) as day_of_week,
        DATE_TRUNC('month', published_date) as month_start,
        DATE_TRUNC('quarter', published_date) as quarter_start,
        DATE_TRUNC('year', published_date) as year_start,
        
        CASE 
            WHEN EXTRACT(MONTH FROM published_date) IN (1,2,3) THEN 'Q1'
            WHEN EXTRACT(MONTH FROM published_date) IN (4,5,6) THEN 'Q2'
            WHEN EXTRACT(MONTH FROM published_date) IN (7,8,9) THEN 'Q3'
            ELSE 'Q4'
        END as quarter_name,
        
        CASE EXTRACT(DAYOFWEEK FROM published_date)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END as day_name,
        
        CASE EXTRACT(MONTH FROM published_date)
            WHEN 1 THEN 'January'
            WHEN 2 THEN 'February'
            WHEN 3 THEN 'March'
            WHEN 4 THEN 'April'
            WHEN 5 THEN 'May'
            WHEN 6 THEN 'June'
            WHEN 7 THEN 'July'
            WHEN 8 THEN 'August'
            WHEN 9 THEN 'September'
            WHEN 10 THEN 'October'
            WHEN 11 THEN 'November'
            WHEN 12 THEN 'December'
        END as month_name
        
    FROM (
        SELECT DISTINCT published_date
        FROM "duckdb"."main_silver"."int_job_title_normalization"
        WHERE published_date IS NOT NULL
    )
)

SELECT
    published_date as date_id,
    year,
    month,
    quarter,
    week,
    day_of_week,
    day_name,
    month_name,
    quarter_name,
    month_start,
    quarter_start,
    year_start,
    NOW() as created_at
FROM date_spine
ORDER BY published_date
    );
  
  