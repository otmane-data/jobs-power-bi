
  
    
    

    create  table
      "duckdb"."main_gold"."fact_job_skills__dbt_tmp"
  
    as (
      -- models/gold/fact_job_skills.sql
-- Gold layer: Bridge Table - Job Skills



WITH skills_raw AS (
    SELECT DISTINCT
        job_url,
        company_name_cleaned,
        skill_name
    FROM "duckdb"."main_silver"."int_skills_extraction"
),

jobs AS (
    SELECT
        job_offer_id,
        job_url
    FROM "duckdb"."main_gold"."fact_job_offers"
),

skills_dim AS (
    SELECT
        skill_id,
        skill_name
    FROM "duckdb"."main_gold"."dim_skills"
),

fact_table AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY s.job_url, sd.skill_id) as job_skill_id,
        j.job_offer_id,
        sd.skill_id,
        s.skill_name,
        NOW() as created_at
    FROM skills_raw s
    LEFT JOIN jobs j ON s.job_url = j.job_url
    LEFT JOIN skills_dim sd ON s.skill_name = sd.skill_name
)

SELECT
    job_skill_id,
    job_offer_id,
    skill_id,
    skill_name,
    created_at
FROM fact_table
WHERE job_offer_id IS NOT NULL
ORDER BY job_offer_id, skill_id
    );
  
  