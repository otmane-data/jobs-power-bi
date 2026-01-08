
-- models/gold/dim_company.sql
-- Gold layer: Dimension Company

{{ config(
    materialized='table',
    schema='gold',
    tags=['gold', 'dimension'],
    unique_id='company_id',
    meta={'owner': 'analytics'}
) }}

WITH jobs AS (
    SELECT DISTINCT
        company_name_cleaned,
        company_url
    FROM {{ ref('int_job_title_normalization') }}
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
