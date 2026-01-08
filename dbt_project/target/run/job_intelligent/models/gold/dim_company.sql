
  
    
    

    create  table
      "duckdb"."main_gold"."dim_company__dbt_tmp"
  
    as (
      -- models/gold/dim_company.sql
-- Gold layer: Dimension Company



WITH jobs AS (
    SELECT DISTINCT
        company_name_cleaned,
        company_url
    FROM "duckdb"."main_silver"."int_job_title_normalization"
    WHERE company_name_cleaned IS NOT NULL
),

ranked_companies AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY company_name_cleaned) as company_id,
        company_name_cleaned as company_name,
        company_url,
        NOW() as created_at
    FROM jobs
)

SELECT
    company_id,
    company_name,
    company_url,
    created_at
FROM ranked_companies
ORDER BY company_id
    );
  
  