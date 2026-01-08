"""
Configuration centralisée pour le système de recommandation
"""
import os
from pathlib import Path

# Chemins des fichiers
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR
MODEL_DIR = Path(__file__).parent / "data" / "models"
EMBEDDINGS_DIR = Path(__file__).parent / "data" / "embeddings"

# Créer les dossiers si nécessaire
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Fichiers de données (Couche Gold)
GOLD_DIR = DATA_DIR / "data" / "gold"
FACT_JOBS_PATH = GOLD_DIR / "fact_job_offers.csv"
DIM_COMPANY_PATH = GOLD_DIR / "dim_company.csv"
DIM_LOCATION_PATH = GOLD_DIR / "dim_location.csv"
FACT_SKILLS_PATH = GOLD_DIR / "fact_job_skills.csv"

# Chemins pour les artefacts du modèle
EMBEDDINGS_PATH = EMBEDDINGS_DIR / "job_embeddings.npy"
JOBS_PROCESSED_PATH = EMBEDDINGS_DIR / "jobs_processed.pkl"
FAISS_INDEX_PATH = EMBEDDINGS_DIR / "faiss_index.bin"

# Configuration du modèle NLP
EMBEDDING_MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"
EMBEDDING_DIMENSION = 512
SPACY_MODEL = "fr_core_news_lg"  # ou "en_core_web_lg" pour anglais

# Compétences techniques communes dans la data et business
# Cette liste contient les noms "canoniques" (affichés à l'utilisateur)
DATA_SKILLS = [
    # Langages de programmation
    'Python', 'R', 'Java', 'Scala', 'Julia', 'C++', 'C#', 'JavaScript', 'TypeScript', 'Node.js',
    'Go', 'Swift', 'Kotlin', 'PHP', 'Ruby', 'Rust', 'MATLAB', 'SAS', 'VBA', 'Fortran',
    
    # Bases de données et SQL
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB',
    'Oracle', 'SQL Server', 'NoSQL', 'Neo4j', 'Elasticsearch', 'MariaDB', 'SQLite',
    'Snowflake', 'BigQuery', 'Redshift', 'Databricks', 'Teradata', 'HBase', 'Hive',
    'Presto', 'Trino',
    
    # Data Engineering / Big Data
    'ETL', 'ELT', 'Data Pipeline', 'Data Warehouse', 'Data Lake', 'Data Mesh', 'Data Fabric',
    'Spark', 'Hadoop', 'Kafka', 'Flink', 'Storm', 'Airflow', 'Luigi', 'Prefect', 'Dagster',
    'dbt', 'Fivetran', 'Stitch', 'Talend', 'Informatica', 'DataStage', 'NiFi', 'HDFS', 'Parquet',
    'Dask', 'Koalas', 'Polars', 'Ray',
    
    # Machine Learning / Deep Learning / AI
    'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 'Natural Language Processing',
    'Computer Vision', 'TensorFlow', 'PyTorch', 'Keras', 'Sklearn', 'XGBoost', 'LightGBM', 'CatBoost',
    'Neural Networks', 'Reinforcement Learning', 'Transfer Learning', 'GANs',
    'Large Language Models', 'GPT', 'BERT', 'Transformers', 'Generative AI',
    'Prompt Engineering', 'LangChain', 'LlamaIndex', 'AutoGPT', 'Vector Database',
    'Pinecone', 'Milvus', 'Weaviate', 'Chroma',
    
    # Data analysis & Statistics
    'Data Analysis', 'Data Analytics', 'Statistics', 'Statistical Modeling', 'Time Series',
    'Forecasting', 'A/B Testing', 'Hypothesis Testing', 'Mathematics', 'Optimization',
    'Operations Research', 'Exploratory Data Analysis', 'Econometrics',
    
    # Data Visualization et BI
    'Tableau', 'Power BI', 'Looker', 'Qlik', 'Metabase', 'Superset', 'Grafana', 'Kibana',
    'D3.js', 'Plotly', 'Matplotlib', 'Seaborn', 'ggplot2', 'MicroStrategy', 'Spotfire',
    'Google Data Studio', 'Looker Studio', 'QuickSight', 'Dashboard', 'Reporting',
    
    # Cloud Platforms
    'AWS', 'Azure', 'GCP', 'Cloud Computing', 'S3', 'EC2', 'Lambda', 'EMR',
    'SageMaker', 'Azure ML', 'Azure Databricks', 'Azure Data Factory', 'Azure Synapse',
    'Cloud Functions', 'Cloud Run', 'Dataflow', 'Dataproc', 'Heroku', 'DigitalOcean',
    
    # DevOps / CI/CD / Infrastructure
    'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Docker', 'Kubernetes', 'Helm',
    'Jenkins', 'CircleCI', 'Travis CI', 'Azure DevOps', 'GitHub Actions',
    'Terraform', 'Ansible', 'CloudFormation', 'Infrastructure as Code',
    'Linux', 'Unix', 'Bash', 'Shell', 'PowerShell',
    
    # Business Analysis & Project Management
    'Business Analysis', 'Business Intelligence', 'Requirements Gathering',
    'Functional Specifications', 'Agile', 'Scrum', 'Kanban', 'Lean', 'Six Sigma',
    'Project Management', 'Product Management', 'Stakeholder Management', 'Jira',
    'Confluence', 'Trello', 'Asana', 'Product Roadmap', 'User Stories', 'SDLC',
    
    # Enterprise Tools (CRM/ERP/...)
    'Salesforce', 'SAP', 'Oracle ERP', 'Dynamics 365', 'Workday', 'ServiceNow',
    'HubSpot', 'Marketo', 'Zendesk', 'NetSuite', 'Alteryx',
    
    # Collaboration & Productivity
    'Excel', 'PowerPoint', 'Word', 'Outlook', 'Office 365',
    'Google Workspace', 'Slack', 'Microsoft Teams', 'SharePoint',
    
    # Soft Skills
    'Communication', 'Leadership', 'Problem Solving', 'Critical Thinking', 'Teamwork',
    'Analytical Thinking', 'Decision Making', 'Time Management', 'Creativity'
]

# Alias pour normaliser les compétences (Alias: Nom Canonique dans DATA_SKILLS)
SKILL_ALIASES = {
    'ai': 'Artificial Intelligence',
    'artificial intelligence': 'Artificial Intelligence',
    'machine learning': 'Machine Learning',
    'ml': 'Machine Learning',
    'nlp': 'Natural Language Processing',
    'natural language processing': 'Natural Language Processing',
    'genai': 'Generative AI',
    'generative ai': 'Generative AI',
    'llm': 'Large Language Models',
    'large language models': 'Large Language Models',
    'microsoft 365': 'Office 365',
    'm365': 'Office 365',
    'office 365': 'Office 365',
    'google cloud platform': 'GCP',
    'google cloud': 'GCP',
    'gcp': 'GCP',
    'amazon web services': 'AWS',
    'aws': 'AWS',
    'microsoft azure': 'Azure',
    'azure': 'Azure',
    't-sql': 'SQL',
    'pl/sql': 'SQL',
    'pyspark': 'Spark',
    'spark': 'Spark',
    'scikit-learn': 'Sklearn',
    'sklearn': 'Sklearn',
    'visual basic': 'VBA',
    'k8s': 'Kubernetes',
    'iac': 'Infrastructure as Code',
    'eda': 'Exploratory Data Analysis',
    'bi': 'Business Intelligence',
    'business intelligence': 'Business Intelligence'
}

# Niveaux d'expérience (pour extraction)
EXPERIENCE_LEVELS = {
    'junior': ['junior', 'entry level', 'entry-level', 'débutant', '0-2 ans', '0-2 years'],
    'mid': ['mid-level', 'intermediate', 'confirmé', '2-5 ans', '3-5 years', '2-5 years'],
    'senior': ['senior', 'expert', 'lead', 'principal', 'staff', '5+ ans', '5+ years', '7+ years'],
    'manager': ['manager', 'head of', 'director', 'vp', 'chief', 'responsable']
}

# Paramètres de scoring
SCORING_WEIGHTS = {
    'semantic_similarity': 0.35,
    'skills_match': 0.25,
    'location_match': 0.20,
    'contract_type_match': 0.05,
    'experience_match': 0.15
}

# Paramètres de recherche
DEFAULT_TOP_K = 10  # Nombre de recommandations par défaut
MAX_TOP_K = 50      # Maximum de recommandations retournées

# Configuration API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True  # Hot reload en développement

# Logs
LOG_LEVEL = "INFO"
