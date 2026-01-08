
  
    
    

    create  table
      "duckdb"."main_gold"."agg_job_offers_by_category_time__dbt_tmp"
  
    as (
      -- models/gold/agg_job_offers_by_category_time.sql
-- Gold layer: Aggregate - Job Offers by Category and Time



SELECT
    f.published_year,
    f.published_month,
    f.published_year_month,
    f.job_category,
    f.contract_type,
    f.work_type,
    
    COUNT(DISTINCT f.job_offer_id) as count_job_offers,
    COUNT(DISTINCT f.company_id) as count_companies,
    
    AVG(f.description_length) as avg_description_length,
    AVG(f.word_count) as avg_word_count,
    
    SUM(CASE WHEN f.is_remote = 1 THEN 1 ELSE 0 END) as remote_jobs,
    SUM(CASE WHEN f.is_permanent = 1 THEN 1 ELSE 0 END) as permanent_jobs,
    
    NOW() as created_at
    
FROM "duckdb"."main_gold"."fact_job_offers" f
WHERE f.published_date IS NOT NULL
GROUP BY
    f.published_year,
    f.published_month,
    f.published_year_month,
    f.job_category,
    f.contract_type,
    f.work_type
ORDER BY f.published_year_month DESC, f.job_category
    );
  
  