
  
    
    

    create  table
      "duckdb"."main_silver"."int_jobs_cleaned__dbt_tmp"
  
    as (
      -- models/silver/int_jobs_cleaned.sql
-- Silver layer: Nettoyage et normalisation des données brutes



WITH raw_jobs AS (
    SELECT * FROM "duckdb"."main_bronze"."stg_jobs_raw"
),

cleaned_jobs AS (
    SELECT
        -- Texte: lowercase, trim, remove special characters
        LOWER(TRIM(job_title)) as job_title_cleaned,
        LOWER(TRIM(location)) as location_cleaned,
        LOWER(TRIM(company_name)) as company_name_cleaned,
        LOWER(TRIM(job_description)) as job_description_cleaned,
        LOWER(TRIM(contract_type)) as contract_type_cleaned,
        LOWER(TRIM(work_type)) as work_type_cleaned,
        
        -- URLs as-is
        job_url,
        company_url,
        
        -- Dates
        TRY_CAST(published_at AS DATE) as published_date,
        posted_time,
        
        -- Extract year-month for time-based analysis
        DATE_TRUNC('month', TRY_CAST(published_at AS DATE)) as published_year_month,
        EXTRACT(YEAR FROM TRY_CAST(published_at AS DATE)) as published_year,
        EXTRACT(MONTH FROM TRY_CAST(published_at AS DATE)) as published_month,
        
        -- Métadonnées
        ingestion_timestamp
    FROM raw_jobs
)

SELECT
    *,
    -- Deduplication flag
    ROW_NUMBER() OVER (
        PARTITION BY job_title_cleaned, company_name_cleaned, location_cleaned 
        ORDER BY published_date DESC
    ) as dedup_rank
FROM cleaned_jobs
    );
  
  