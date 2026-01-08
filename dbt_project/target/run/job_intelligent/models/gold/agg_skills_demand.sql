
  
    
    

    create  table
      "duckdb"."main_gold"."agg_skills_demand__dbt_tmp"
  
    as (
      -- models/gold/agg_skills_demand.sql
-- Gold layer: Aggregate - Skills in Demand



SELECT
    sd.skill_id,
    sd.skill_name,
    sd.skill_category,
    
    COUNT(DISTINCT fs.job_offer_id) as count_jobs_requiring_skill,
    COUNT(DISTINCT f.company_id) as count_companies_requiring_skill,
    
    -- Percentage of all jobs
    ROUND(
        100.0 * COUNT(DISTINCT fs.job_offer_id) / (
            SELECT COUNT(DISTINCT job_offer_id) FROM "duckdb"."main_gold"."fact_job_offers"
        ),
        2
    ) as pct_of_total_jobs,
    
    -- Average job details for jobs requiring this skill
    AVG(f.description_length) as avg_description_length,
    AVG(f.word_count) as avg_word_count,
    
    NOW() as created_at
    
FROM "duckdb"."main_gold"."dim_skills" sd
LEFT JOIN "duckdb"."main_gold"."fact_job_skills" fs ON sd.skill_id = fs.skill_id
LEFT JOIN "duckdb"."main_gold"."fact_job_offers" f ON fs.job_offer_id = f.job_offer_id
GROUP BY
    sd.skill_id,
    sd.skill_name,
    sd.skill_category
ORDER BY count_jobs_requiring_skill DESC
    );
  
  