-- models/bronze/stg_jobs_raw.sql
-- Bronze layer: Lecture directe des données brutes depuis final_data.csv
-- Renommage et typage minimal



-- Read directly from CSV file
SELECT
    -- Renommer les colonnes pour cohérence
    title as job_title,
    location,
    postedTime as posted_time,
    publishedAt as published_at,
    jobUrl as job_url,
    companyName as company_name,
    companyUrl as company_url,
    description as job_description,
    contractType as contract_type,
    workType as work_type,
    
    -- Métadonnées de traçabilité
    NOW() as ingestion_timestamp,
    '2026-01-08 10:38:46.135216+00:00' as dbt_run_id

FROM read_csv_auto('D:/lab2/final_data.csv')

WHERE 1=1
    -- Filtrer les lignes vides
    AND title IS NOT NULL
    AND description IS NOT NULL