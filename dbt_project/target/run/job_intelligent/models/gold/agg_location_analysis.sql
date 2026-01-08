
  
    
    

    create  table
      "duckdb"."main_gold"."agg_location_analysis__dbt_tmp"
  
    as (
      -- models/gold/agg_location_analysis.sql
-- Gold layer: Aggregate - Location Analysis



SELECT
    dl.location_id,
    dl.location_raw,
    dl.city,
    dl.country,
    dl.work_location_type,
    
    COUNT(DISTINCT f.job_offer_id) as count_job_offers,
    COUNT(DISTINCT f.company_id) as count_companies,
    
    -- Distribution by job category
    COUNT(DISTINCT CASE WHEN f.job_category = 'Data Engineer' THEN f.job_offer_id END) as data_engineer_count,
    COUNT(DISTINCT CASE WHEN f.job_category = 'Data Scientist' THEN f.job_offer_id END) as data_scientist_count,
    COUNT(DISTINCT CASE WHEN f.job_category = 'Data Analyst' THEN f.job_offer_id END) as data_analyst_count,
    COUNT(DISTINCT CASE WHEN f.job_category = 'ML Engineer' THEN f.job_offer_id END) as ml_engineer_count,
    
    -- Remote percentage
    ROUND(
        100.0 * SUM(CASE WHEN f.is_remote = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT f.job_offer_id),
        2
    ) as pct_remote,
    
    NOW() as created_at
    
FROM "duckdb"."main_gold"."dim_location" dl
LEFT JOIN "duckdb"."main_gold"."fact_job_offers" f ON dl.location_id = f.location_id
GROUP BY
    dl.location_id,
    dl.location_raw,
    dl.city,
    dl.country,
    dl.work_location_type
ORDER BY count_job_offers DESC
    );
  
  