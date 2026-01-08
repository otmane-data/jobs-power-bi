-- models/gold/fact_job_offers.sql
-- Gold layer: Fact Table - Job Offers (Schéma en Étoile)



WITH jobs AS (
    SELECT
        j.*
    FROM "duckdb"."main_silver"."int_job_title_normalization" j
),

companies AS (
    SELECT * FROM "duckdb"."main_gold"."dim_company"
),

locations AS (
    SELECT * FROM "duckdb"."main_gold"."dim_location"
),

times AS (
    SELECT * FROM "duckdb"."main_gold"."dim_time"
),

fact_table AS (
    SELECT
        -- Surrogate keys
        ROW_NUMBER() OVER (ORDER BY j.job_url, j.company_name_cleaned) as job_offer_id,
        
        -- Foreign keys
        c.company_id,
        l.location_id,
        t.date_id as published_date_id,
        
        -- Job dimensions
        j.job_title_cleaned as job_title,
        j.job_category,
        j.contract_type_normalized as contract_type,
        j.work_type_normalized as work_type,
        
        -- URLs
        j.job_url,
        j.company_url,
        
        -- Description
        j.job_description_cleaned as job_description,
        
        -- Time dimension
        j.published_date,
        j.posted_time,
        j.published_year_month,
        j.published_year,
        j.published_month,
        
        -- Metrics
        LENGTH(j.job_description_cleaned) as description_length,
        (LENGTH(j.job_description_cleaned) - LENGTH(REPLACE(j.job_description_cleaned, ' ', ''))) + 1 as word_count,
        
        -- Flags
        CASE WHEN j.work_type_normalized = 'Remote' THEN 1 ELSE 0 END as is_remote,
        CASE WHEN j.contract_type_normalized = 'Permanent' THEN 1 ELSE 0 END as is_permanent,
        
        -- Metadata
        NOW() as created_at,
        j.ingestion_timestamp
        
    FROM jobs j
    LEFT JOIN companies c ON j.company_name_cleaned = c.company_name
    LEFT JOIN locations l ON j.location_cleaned = l.location_raw
    LEFT JOIN times t ON j.published_date = t.date_id
)

SELECT
    job_offer_id,
    company_id,
    location_id,
    published_date_id,
    job_title,
    job_category,
    contract_type,
    work_type,
    job_url,
    company_url,
    job_description,
    published_date,
    posted_time,
    published_year_month,
    published_year,
    published_month,
    description_length,
    word_count,
    is_remote,
    is_permanent,
    created_at,
    ingestion_timestamp
FROM fact_table
ORDER BY published_date DESC, job_offer_id