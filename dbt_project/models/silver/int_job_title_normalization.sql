
-- models/silver/int_job_title_normalization.sql
-- Silver layer: Normaliser les intitulés de postes

{{ config(
    materialized='table',
    schema='silver',
    tags=['silver', 'normalization'],
    meta={'owner': 'data_engineering'}
) }}

WITH cleaned_jobs AS (
    SELECT * FROM {{ ref('int_jobs_cleaned') }}
),

title_normalized AS (
    SELECT
        *,
        CASE
            WHEN job_title_cleaned LIKE '%data engineer%' THEN 'Data Engineer'
            WHEN job_title_cleaned LIKE '%data scientist%' THEN 'Data Scientist'
            WHEN job_title_cleaned LIKE '%data analyst%' THEN 'Data Analyst'
            WHEN job_title_cleaned LIKE '%analytics engineer%' THEN 'Analytics Engineer'
            WHEN job_title_cleaned LIKE '%ml engineer%' OR job_title_cleaned LIKE '%machine learning%' THEN 'ML Engineer'
            WHEN job_title_cleaned LIKE '%data architect%' THEN 'Data Architect'
            WHEN job_title_cleaned LIKE '%bi developer%' OR job_title_cleaned LIKE '%business intelligence%' THEN 'BI Developer'
            WHEN job_title_cleaned LIKE '%etl%' OR job_title_cleaned LIKE '%pipeline%' THEN 'ETL/Pipeline Engineer'
            WHEN job_title_cleaned LIKE '%data engineer%' THEN 'Data Engineer'
            ELSE 'Other Data Role'
        END as job_category,
        
        CASE
            WHEN contract_type_cleaned LIKE '%cdi%' OR contract_type_cleaned LIKE '%permanent%' THEN 'Permanent'
            WHEN contract_type_cleaned LIKE '%cdd%' OR contract_type_cleaned LIKE '%contract%' THEN 'Contract'
            WHEN contract_type_cleaned LIKE '%stage%' OR contract_type_cleaned LIKE '%internship%' THEN 'Internship'
            WHEN contract_type_cleaned LIKE '%freelance%' THEN 'Freelance'
            ELSE 'Not Specified'
        END as contract_type_normalized,
        
        CASE
            WHEN work_type_cleaned LIKE '%remote%' THEN 'Remote'
            WHEN work_type_cleaned LIKE '%hybrid%' THEN 'Hybrid'
            WHEN work_type_cleaned LIKE '%onsite%' OR work_type_cleaned LIKE '%on-site%' THEN 'On-site'
            ELSE 'Not Specified'
        END as work_type_normalized
    
    FROM cleaned_jobs
    WHERE dedup_rank = 1  -- Keep only first occurrence (most recent)
)

SELECT * FROM title_normalized
