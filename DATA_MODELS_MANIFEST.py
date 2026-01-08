"""
JOB INTELLIGENT - Data Models Manifest
Liste complète de tous les modèles DBT et leurs propriétés
"""

MANIFEST = {
    "project_name": "JOB INTELLIGENT",
    "description": "Centralisation des offres Data et Système de Recommandation",
    "version": "1.0.0",
    "created_date": "2026-01-07",
    "last_modified": "2026-01-07",
    "data_source": "LinkedIn Job Postings (final_data.csv)",
    "total_job_offers": 131570,
    
    # ==================== BRONZE LAYER ====================
    "bronze_layer": {
        "description": "Raw data layer - Direct read from CSV",
        "materialization": "VIEW",
        "models": {
            "stg_jobs_raw": {
                "type": "VIEW",
                "source": "final_data.csv",
                "row_count": "~131K",
                "columns": [
                    "job_title",
                    "location",
                    "posted_time",
                    "published_at",
                    "job_url",
                    "company_name",
                    "company_url",
                    "job_description",
                    "contract_type",
                    "work_type",
                    "ingestion_timestamp",
                    "dbt_run_id"
                ],
                "operations": [
                    "CSV read with read_csv_auto()",
                    "Column renaming",
                    "Empty row filtering",
                    "Metadata addition"
                ]
            }
        }
    },
    
    # ==================== SILVER LAYER ====================
    "silver_layer": {
        "description": "Cleaned and normalized data layer",
        "materialization": "TABLE",
        "models": {
            "int_jobs_cleaned": {
                "type": "TABLE",
                "parent": "stg_jobs_raw",
                "row_count": "~131K",
                "description": "Text cleanup, standardization, date parsing",
                "columns": [
                    "job_title_cleaned",      # lowercase, trim
                    "location_cleaned",       # lowercase, trim
                    "company_name_cleaned",   # lowercase, trim
                    "job_description_cleaned",# lowercase, trim
                    "contract_type_cleaned",  # lowercase, trim
                    "work_type_cleaned",      # lowercase, trim
                    "job_url",
                    "company_url",
                    "published_date",         # casted to DATE
                    "posted_time",
                    "published_year_month",   # date_trunc
                    "published_year",         # extract year
                    "published_month",        # extract month
                    "dedup_rank",             # for deduplication
                    "ingestion_timestamp"
                ],
                "operations": [
                    "LOWER() + TRIM() on text",
                    "TRY_CAST dates",
                    "DATE_TRUNC for aggregations",
                    "EXTRACT year/month",
                    "ROW_NUMBER for deduplication"
                ],
                "unique_key": ["dedup_rank = 1"]
            },
            
            "int_job_title_normalization": {
                "type": "TABLE",
                "parent": "int_jobs_cleaned",
                "row_count": "~100K",
                "description": "Job category, contract type, work type normalization",
                "columns": [
                    "job_title_cleaned",
                    "job_category",           # normalized job role
                    "contract_type_normalized",
                    "work_type_normalized",
                    "location_cleaned",
                    "company_name_cleaned",
                    "published_date",
                    "published_year_month",
                    "all_previous_columns"
                ],
                "job_categories": [
                    "Data Engineer",
                    "Data Scientist",
                    "Data Analyst",
                    "ML Engineer",
                    "Analytics Engineer",
                    "BI Developer",
                    "ETL/Pipeline Engineer",
                    "Data Architect",
                    "Other Data Role"
                ],
                "contract_types": [
                    "Permanent",
                    "Contract",
                    "Internship",
                    "Freelance",
                    "Not Specified"
                ],
                "work_types": [
                    "Remote",
                    "Hybrid",
                    "On-site",
                    "Not Specified"
                ],
                "operations": [
                    "CASE normalization for job titles",
                    "CASE normalization for contract types",
                    "CASE normalization for work types",
                    "Deduplication (dedup_rank = 1)"
                ]
            },
            
            "int_skills_extraction": {
                "type": "TABLE",
                "parent": "int_job_title_normalization",
                "row_count": "~500K",
                "description": "Extract technical skills from job descriptions",
                "columns": [
                    "job_title_cleaned",
                    "location_cleaned",
                    "company_name_cleaned",
                    "skill_name",
                    "has_skill",
                    "published_date",
                    "job_category",
                    "all_previous_columns"
                ],
                "skills_mapped": [
                    "Python", "SQL", "Spark", "Hadoop", "Scala", "Java", "R",
                    "Tableau", "Power BI", "Looker",
                    "AWS", "Azure", "GCP",
                    "Airflow", "DBT", "Kubernetes", "Docker",
                    "Git", "TensorFlow", "PyTorch", "Scikit-learn",
                    "Pandas", "NumPy",
                    "Machine Learning", "Statistics", "Data Visualization"
                ],
                "total_skills_in_mapping": 25,
                "operations": [
                    "CROSS JOIN with skills mapping table",
                    "Regex pattern matching (~* operator)",
                    "Filter where has_skill = 1",
                    "UNION ALL skill definitions"
                ]
            }
        }
    },
    
    # ==================== GOLD LAYER ====================
    "gold_layer": {
        "description": "Analytics-ready data layer with star schema",
        "materialization": "TABLE",
        
        "dimensions": {
            "dim_time": {
                "type": "DIMENSION",
                "row_count": "~2,000",
                "primary_key": "date_id",
                "columns": [
                    "date_id",           # date (PK)
                    "year",
                    "month",
                    "quarter",
                    "week",
                    "day_of_week",       # 0-6 (Sunday=0)
                    "day_name",          # 'Monday', etc.
                    "month_name",        # 'January', etc.
                    "quarter_name",      # 'Q1', etc.
                    "month_start",       # date trunc to month
                    "quarter_start",     # date trunc to quarter
                    "year_start",        # date trunc to year
                    "created_at"
                ],
                "relationships": [
                    "← fact_job_offers[published_date_id]"
                ]
            },
            
            "dim_company": {
                "type": "DIMENSION",
                "row_count": "~5,000",
                "primary_key": "company_id",
                "columns": [
                    "company_id",        # integer (PK)
                    "company_name",
                    "company_url",
                    "created_at"
                ],
                "relationships": [
                    "← fact_job_offers[company_id]"
                ]
            },
            
            "dim_location": {
                "type": "DIMENSION",
                "row_count": "~3,000",
                "primary_key": "location_id",
                "columns": [
                    "location_id",       # integer (PK)
                    "location_raw",      # original string
                    "city",              # parsed from location_raw
                    "country",           # parsed from location_raw
                    "work_location_type",# 'Remote' or 'On-site'
                    "created_at"
                ],
                "relationships": [
                    "← fact_job_offers[location_id]"
                ]
            },
            
            "dim_skills": {
                "type": "DIMENSION",
                "row_count": "~30",
                "primary_key": "skill_id",
                "columns": [
                    "skill_id",          # integer (PK)
                    "skill_name",
                    "skill_category",    # 'Programming Language', 'Cloud', etc.
                    "created_at"
                ],
                "skill_categories": [
                    "Programming Language",
                    "Database",
                    "Big Data Framework",
                    "ML/DL Library",
                    "Cloud Platform",
                    "BI Tool",
                    "DataOps/DevOps",
                    "Data Analysis Library",
                    "Domain Knowledge",
                    "Other"
                ],
                "relationships": [
                    "← fact_job_skills[skill_id]"
                ]
            }
        },
        
        "facts": {
            "fact_job_offers": {
                "type": "FACT",
                "row_count": "~100,000",
                "surrogate_key": "job_offer_id",
                "foreign_keys": [
                    "company_id → dim_company",
                    "location_id → dim_location",
                    "published_date_id → dim_time"
                ],
                "columns": {
                    "surrogates": [
                        "job_offer_id"
                    ],
                    "dimensions": [
                        "company_id",
                        "location_id",
                        "published_date_id",
                        "job_title",
                        "job_category",
                        "contract_type",
                        "work_type"
                    ],
                    "attributes": [
                        "job_url",
                        "company_url",
                        "job_description",
                        "published_date",
                        "posted_time",
                        "published_year_month",
                        "published_year",
                        "published_month"
                    ],
                    "metrics": [
                        "description_length",  # calculated: LENGTH(job_description)
                        "word_count",          # calculated: space count + 1
                        "is_remote",           # flag: 0/1
                        "is_permanent",        # flag: 0/1
                    ]
                },
                "relationships": [
                    "→ fact_job_skills[job_offer_id]"
                ]
            },
            
            "fact_job_skills": {
                "type": "FACT (Bridge Table)",
                "row_count": "~500,000",
                "surrogate_key": "job_skill_id",
                "foreign_keys": [
                    "job_offer_id → fact_job_offers",
                    "skill_id → dim_skills"
                ],
                "columns": [
                    "job_skill_id",
                    "job_offer_id",
                    "skill_id",
                    "skill_name",        # denormalized for ease
                    "created_at"
                ],
                "purpose": "Many-to-Many relationship between jobs and skills"
            }
        },
        
        "aggregates": {
            "agg_job_offers_by_category_time": {
                "type": "AGGREGATE",
                "row_count": "~5,000",
                "description": "Job offers aggregated by time and category",
                "grain": "Year-Month-JobCategory-ContractType-WorkType",
                "dimensions": [
                    "published_year",
                    "published_month",
                    "published_year_month",
                    "job_category",
                    "contract_type",
                    "work_type"
                ],
                "metrics": [
                    "count_job_offers",
                    "count_companies",
                    "avg_description_length",
                    "avg_word_count",
                    "remote_jobs",
                    "permanent_jobs"
                ],
                "use_case": "Time series analysis, trend visualization"
            },
            
            "agg_skills_demand": {
                "type": "AGGREGATE",
                "row_count": "~30",
                "description": "Skills demand ranking",
                "grain": "SkillName-SkillCategory",
                "dimensions": [
                    "skill_id",
                    "skill_name",
                    "skill_category"
                ],
                "metrics": [
                    "count_jobs_requiring_skill",
                    "count_companies_requiring_skill",
                    "pct_of_total_jobs",
                    "avg_description_length"
                ],
                "use_case": "Identify most sought-after skills"
            },
            
            "agg_location_analysis": {
                "type": "AGGREGATE",
                "row_count": "~3,000",
                "description": "Jobs distribution by location",
                "grain": "LocationId-City-Country",
                "dimensions": [
                    "location_id",
                    "location_raw",
                    "city",
                    "country",
                    "work_location_type"
                ],
                "metrics": [
                    "count_job_offers",
                    "count_companies",
                    "data_engineer_count",
                    "data_scientist_count",
                    "data_analyst_count",
                    "ml_engineer_count",
                    "pct_remote"
                ],
                "use_case": "Geographic analysis, market sizing"
            }
        }
    },
    
    # ==================== STATISTICS ====================
    "statistics": {
        "total_job_records": 131570,
        "estimated_distinct_companies": 5000,
        "estimated_distinct_locations": 3000,
        "estimated_distinct_skills": 25,
        "estimated_skill_mentions": 500000,
        "date_range": "Varies by scrape date",
        "data_quality": {
            "completeness_estimate": "95%",
            "notes": [
                "Some descriptions may be truncated",
                "Some locations may be generic",
                "Skills extraction based on pattern matching"
            ]
        }
    },
    
    # ==================== TRANSFORMATION RULES ====================
    "transformation_rules": {
        "text_normalization": {
            "operation": "LOWER(TRIM(field))",
            "purpose": "Standard case and remove whitespace"
        },
        "date_parsing": {
            "operation": "TRY_CAST(date_field AS DATE)",
            "null_handling": "Keep as NULL if unparseable"
        },
        "deduplication": {
            "method": "ROW_NUMBER() OVER PARTITION BY key COLUMNS ORDER BY date DESC",
            "keep": "Most recent record (rank = 1)"
        },
        "skill_extraction": {
            "method": "Regex pattern matching with ~* operator",
            "case_sensitive": False,
            "note": "May require manual verification"
        }
    }
}

# Export for reference
if __name__ == "__main__":
    import json
    print(json.dumps(MANIFEST, indent=2))
