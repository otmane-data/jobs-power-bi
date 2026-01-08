
  
    
    

    create  table
      "duckdb"."main_silver"."int_skills_extraction__dbt_tmp"
  
    as (
      -- models/silver/int_skills_extraction.sql
-- Silver layer: Extraction des compétences depuis la description



WITH jobs_with_titles AS (
    SELECT * FROM "duckdb"."main_silver"."int_job_title_normalization"
),

skills_mapping AS (
    -- Définir un mapping de compétences communes Data/Tech
    SELECT
        'Python' as skill_name,
        'python|py |\.py' as skill_pattern
    UNION ALL SELECT 'SQL', 'sql|sql|sql server|postgres|oracle'
    UNION ALL SELECT 'Spark', 'spark|pyspark'
    UNION ALL SELECT 'Hadoop', 'hadoop|hdfs'
    UNION ALL SELECT 'Scala', 'scala'
    UNION ALL SELECT 'Java', '\bjava\b'
    UNION ALL SELECT 'R', '\br\b|r programming'
    UNION ALL SELECT 'Tableau', 'tableau'
    UNION ALL SELECT 'Power BI', 'power bi|powerbi'
    UNION ALL SELECT 'Looker', 'looker'
    UNION ALL SELECT 'AWS', 'aws|amazon web|s3 |ec2|redshift'
    UNION ALL SELECT 'Azure', 'azure|microsoft azure|synapse|cosmos'
    UNION ALL SELECT 'GCP', 'gcp|google cloud|bigquery'
    UNION ALL SELECT 'Airflow', 'airflow'
    UNION ALL SELECT 'DBT', '\bdbt\b|dbt'
    UNION ALL SELECT 'Kubernetes', 'kubernetes|k8s'
    UNION ALL SELECT 'Docker', 'docker'
    UNION ALL SELECT 'Git', 'git|github|gitlab'
    UNION ALL SELECT 'TensorFlow', 'tensorflow'
    UNION ALL SELECT 'PyTorch', 'pytorch'
    UNION ALL SELECT 'Scikit-learn', 'scikit|sklearn'
    UNION ALL SELECT 'Pandas', 'pandas'
    UNION ALL SELECT 'NumPy', 'numpy'
    UNION ALL SELECT 'Machine Learning', 'machine learning|deep learning|ml|artificial intelligence'
    UNION ALL SELECT 'Statistics', 'statistics|statistical|probability'
    UNION ALL SELECT 'Data Visualization', 'data visualization|visualization|charts|graphs'
),

jobs_exploded AS (
    SELECT
        j.*,
        s.skill_name,
        CASE 
            WHEN job_description_cleaned ILIKE '%' || s.skill_pattern || '%' THEN 1 
            ELSE 0 
        END as has_skill
    FROM jobs_with_titles j
    CROSS JOIN skills_mapping s
)

SELECT
    *
FROM jobs_exploded
WHERE has_skill = 1

ORDER BY job_title_cleaned, published_date DESC
    );
  
  