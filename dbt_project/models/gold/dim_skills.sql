
-- models/gold/dim_skills.sql
-- Gold layer: Dimension Skills

{{ config(
    materialized='table',
    schema='gold',
    tags=['gold', 'dimension'],
    unique_id='skill_id',
    meta={'owner': 'analytics'}
) }}

WITH skills AS (
    SELECT DISTINCT
        skill_name
    FROM {{ ref('int_skills_extraction') }}
    WHERE skill_name IS NOT NULL
),

skill_categorization AS (
    SELECT
        skill_name,
        CASE
            WHEN skill_name IN ('Python', 'Java', 'Scala', 'R') THEN 'Programming Language'
            WHEN skill_name IN ('SQL', 'NoSQL') THEN 'Database'
            WHEN skill_name IN ('Spark', 'Hadoop', 'Hive', 'Kafka') THEN 'Big Data Framework'
            WHEN skill_name IN ('TensorFlow', 'PyTorch', 'Scikit-learn') THEN 'ML/DL Library'
            WHEN skill_name IN ('AWS', 'Azure', 'GCP') THEN 'Cloud Platform'
            WHEN skill_name IN ('Tableau', 'Power BI', 'Looker') THEN 'BI Tool'
            WHEN skill_name IN ('Airflow', 'DBT', 'Kubernetes', 'Docker') THEN 'DataOps/DevOps'
            WHEN skill_name IN ('Pandas', 'NumPy', 'Matplotlib') THEN 'Data Analysis Library'
            WHEN skill_name IN ('Machine Learning', 'Statistics', 'Data Visualization') THEN 'Domain Knowledge'
            ELSE 'Other'
        END as skill_category
    FROM skills
),

ranked_skills AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY skill_name) as skill_id,
        skill_name,
        skill_category,
        NOW() as created_at
    FROM skill_categorization
)

SELECT
    skill_id,
    skill_name,
    skill_category,
    created_at
FROM ranked_skills
ORDER BY skill_id
