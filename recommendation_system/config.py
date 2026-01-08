"""
Configuration centralisée pour le système de recommandation
"""
import os
from pathlib import Path

# Chemins des fichiers
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "jobs-power-bi"
MODEL_DIR = Path(__file__).parent / "data" / "models"
EMBEDDINGS_DIR = Path(__file__).parent / "data" / "embeddings"

# Créer les dossiers si nécessaire
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Fichiers de données
JOBS_CSV_PATH = DATA_DIR / "final_data.csv"
EMBEDDINGS_PATH = EMBEDDINGS_DIR / "job_embeddings.npy"
JOBS_PROCESSED_PATH = EMBEDDINGS_DIR / "jobs_processed.pkl"
FAISS_INDEX_PATH = EMBEDDINGS_DIR / "faiss_index.bin"

# Configuration du modèle NLP
EMBEDDING_MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"
EMBEDDING_DIMENSION = 512
SPACY_MODEL = "fr_core_news_lg"  # ou "en_core_web_lg" pour anglais

# Compétences techniques communes dans la data
DATA_SKILLS = [
    # Langages de programmation
    'Python', 'R', 'Java', 'Scala', 'Julia', 'C++', 'JavaScript', 'TypeScript',
    
    # Bases de données et SQL
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB',
    'Oracle', 'SQL Server', 'NoSQL', 'Neo4j', 'Elasticsearch',
    
    # Big Data
    'Spark', 'Hadoop', 'Kafka', 'Flink', 'Storm', 'Hive', 'Pig', 'HBase',
    'Databricks', 'Snowflake', 'Redshift', 'BigQuery',
    
    # Machine Learning / Deep Learning
    'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP', 'Computer Vision',
    'TensorFlow', 'PyTorch', 'Keras', 'scikit-learn', 'XGBoost', 'LightGBM',
    'Random Forest', 'Regression', 'Classification', 'Clustering',
    'Reinforcement Learning', 'Transfer Learning', 'GANs', 'Transformers',
    'BERT', 'GPT', 'LLM', 'Large Language Models',
    
    # Data Engineering
    'ETL', 'ELT', 'Data Pipeline', 'Data Warehouse', 'Data Lake', 'Data Mesh',
    'Airflow', 'Luigi', 'Prefect', 'dbt', 'Fivetran', 'Stitch',
    
    # Cloud Platforms
    'AWS', 'Azure', 'GCP', 'Google Cloud', 'Amazon Web Services', 'Microsoft Azure',
    'S3', 'EC2', 'Lambda', 'EMR', 'Glue', 'SageMaker', 'Kinesis',
    'Azure ML', 'Azure Databricks', 'Azure Data Factory', 'Azure Synapse',
    'BigQuery', 'Cloud Functions', 'Cloud Run', 'Dataflow', 'Dataproc',
    
    # Conteneurisation et Orchestration
    'Docker', 'Kubernetes', 'K8s', 'Helm', 'Docker Compose',
    
    # CI/CD et Version Control
    'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'CircleCI', 'Travis CI',
    'Azure DevOps', 'GitOps', 'Terraform', 'Ansible', 'CloudFormation',
    
    # Data Visualization et BI
    'Tableau', 'Power BI', 'Looker', 'Qlik', 'Metabase', 'Superset',
    'D3.js', 'Plotly', 'Matplotlib', 'Seaborn', 'ggplot2',
    
    # Python Libraries
    'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'Plotly',
    'Jupyter', 'Notebook', 'PySpark', 'Dask', 'Polars',
    
    # MLOps
    'MLflow', 'Kubeflow', 'MLOps', 'Model Registry', 'Feature Store',
    'Weights & Biases', 'Neptune.ai', 'DVC',
    
    # API et Web
    'REST API', 'FastAPI', 'Flask', 'Django', 'GraphQL', 'gRPC',
    
    # Statistiques et Math
    'Statistics', 'Statistical Modeling', 'Time Series', 'Forecasting',
    'A/B Testing', 'Hypothesis Testing', 'Bayesian Statistics',
    
    # Méthodologies
    'Agile', 'Scrum', 'Kanban', 'DevOps', 'DataOps', 'CI/CD',
    
    # Autres
    'Excel', 'VBA', 'SAP', 'Salesforce', 'Jira', 'Confluence'
]

# Niveaux d'expérience (pour extraction)
EXPERIENCE_LEVELS = {
    'junior': ['junior', 'entry level', 'entry-level', 'débutant', '0-2 ans', '0-2 years'],
    'mid': ['mid-level', 'intermediate', 'confirmé', '2-5 ans', '3-5 years', '2-5 years'],
    'senior': ['senior', 'expert', 'lead', 'principal', 'staff', '5+ ans', '5+ years', '7+ years'],
    'manager': ['manager', 'head of', 'director', 'vp', 'chief', 'responsable']
}

# Paramètres de scoring
SCORING_WEIGHTS = {
    'semantic_similarity': 0.50,  # Similarité sémantique globale
    'skills_match': 0.25,         # Correspondance des compétences
    'location_match': 0.10,       # Compatibilité localisation
    'contract_type_match': 0.10,  # Type de contrat
    'experience_match': 0.05      # Niveau d'expérience
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
