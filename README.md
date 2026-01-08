# JOB INTELLIGENT - Système de Centralisation et Recommandation d'Offres Data

![Status](https://img.shields.io/badge/Status-Active-green) ![Version](https://img.shields.io/badge/Version-1.0-blue)

**Un projet complet de Data Engineering & Analytics pour l'analyse et la recommandation d'offres d'emploi Data.**

---

## 📚 Table des Matières

- [Objectif du Projet](#-objectif-du-projet)
- [Architecture](#-architecture)
- [Structure du Projet](#-structure-du-projet)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [DBT Models](#-dbt-models)
- [Power BI](#-power-bi)
- [Documentation](#-documentation)
- [Licence](#-licence)

---

## 🎯 Objectif du Projet

**Centraliser et analyser les offres d'emploi Data** en provenance de LinkedIn (131 570 offres) pour :

1. ✅ Créer une structure analytique professionnelle (Bronze/Silver/Gold)
2. ✅ Nettoyer et transformer les données avec **DBT**
3. ✅ Extraire les insights business (compétences, tendances, géographie)
4. ✅ Créer des dashboards interactifs avec **Power BI**
5. ✅ Préparer un système de recommandation d'offres (**Phase 2**)

### Contraintes du Projet
- ✓ **100% Local** (pas de cloud)
- ✓ **Sans Airflow** (orchestration manuelle/Python)
- ✓ **Sans Docker**
- ✓ **Sans PostgreSQL** (fichiers locaux)
- ✓ **Transformation DBT** obligatoire
- ✓ **BI avec Power BI**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SOURCE LAYER                             │
│                    final_data.csv (131K rows)                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER                               │
│              (Raw data + basic renaming)                        │
│                                                                 │
│  • stg_jobs_raw                                                │
│  • Materialization: VIEW                                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SILVER LAYER                               │
│          (Cleaning, Normalization, Enrichment)                 │
│                                                                 │
│  • int_jobs_cleaned                                            │
│  • int_job_title_normalization                                │
│  • int_skills_extraction                                       │
│  • Materialization: TABLE                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                      GOLD LAYER                                 │
│             (Analytics-ready + Star Schema)                    │
│                                                                 │
│  Dimensions:                                                   │
│  • dim_time (2K rows)                                          │
│  • dim_company (5K rows)                                       │
│  • dim_location (3K rows)                                      │
│  • dim_skills (30 rows)                                        │
│                                                                 │
│  Facts:                                                        │
│  • fact_job_offers (100K rows)                                 │
│  • fact_job_skills (500K rows)                                │
│                                                                 │
│  Aggregates:                                                   │
│  • agg_job_offers_by_category_time                             │
│  • agg_skills_demand                                           │
│  • agg_location_analysis                                       │
│                                                                 │
│  • Materialization: TABLE                                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    POWER BI (Visualizations)                    │
│                                                                 │
│  Pages:                                                        │
│  • Overview Dashboard                                          │
│  • Job Categories Analysis                                    │
│  • Skills Demand                                              │
│  • Geographic Analysis                                        │
│  • Company Analysis                                           │
│  • Advanced Analytics                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure du Projet

```
lab2/
├── 📄 final_data.csv                    # ← Source data
├── 📄 README.md                         # ← Ce fichier
├── 📄 ARCHITECTURE.md                   # ← Documentation architecture
├── 📄 POWER_BI_GUIDE.md                # ← Guide Power BI détaillé
├── 🐍 run_pipeline.py                   # ← Script orchestration Python
│
├── data/
│   ├── bronze/                          # ← Couche brutes
│   │   └── final_data.csv              # (Copié automatiquement)
│   ├── silver/                          # ← Couche nettoyée
│   └── gold/                            # ← Couche analytique (exported CSV)
│       ├── dim_time.csv
│       ├── dim_company.csv
│       ├── dim_location.csv
│       ├── dim_skills.csv
│       ├── fact_job_offers.csv
│       ├── fact_job_skills.csv
│       ├── agg_job_offers_by_category_time.csv
│       ├── agg_skills_demand.csv
│       └── agg_location_analysis.csv
│
└── dbt_project/
    ├── dbt_project.yml                  # Configuration DBT
    ├── profiles.yml                     # Connecteurs database
    ├── target/                          # DBT build output
    │   └── duckdb.db                   # (Généré après dbt run)
    │
    ├── models/
    │   ├── bronze/
    │   │   └── stg_jobs_raw.sql
    │   │
    │   ├── silver/
    │   │   ├── int_jobs_cleaned.sql
    │   │   ├── int_job_title_normalization.sql
    │   │   └── int_skills_extraction.sql
    │   │
    │   └── gold/
    │       ├── dim_time.sql
    │       ├── dim_company.sql
    │       ├── dim_location.sql
    │       ├── dim_skills.sql
    │       ├── fact_job_offers.sql
    │       ├── fact_job_skills.sql
    │       ├── agg_job_offers_by_category_time.sql
    │       ├── agg_skills_demand.sql
    │       └── agg_location_analysis.sql
    │
    ├── tests/                          # Tests DBT
    ├── macros/                         # Macros réutilisables
    ├── analyses/                       # Analyses ad-hoc
    └── docs/                           # Documentation DBT
```

---

## 🚀 Installation

### Prérequis

```bash
# Python 3.8+
python --version

# Packages
pip install dbt-core dbt-duckdb pandas openpyxl
```

### Étapes

1. **Cloner/Télécharger le projet**
   ```bash
   cd d:\lab2
   ```

2. **Installer les dépendances DBT**
   ```bash
   cd dbt_project
   dbt debug
   ```

3. **Vérifier la configuration**
   ```bash
   # Vérifier que final_data.csv est présent
   ls -la final_data.csv
   ```

---

## 💻 Utilisation

### Option 1 : Utiliser le script Python (Recommandé)

```bash
# Depuis d:\lab2
python run_pipeline.py
```

**Ce script fait automatiquement** :
1. ✓ Vérifie les dépendances
2. ✓ Copie les données source en Bronze
3. ✓ Exécute `dbt run`
4. ✓ Exécute les tests DBT
5. ✓ Exporte les tables Gold en CSV
6. ✓ Génère un rapport final

### Option 2 : Exécution manuelle DBT

```bash
cd dbt_project

# Debug
dbt debug

# Run
dbt run

# Test (optionnel)
dbt test

# Docs (optionnel)
dbt docs generate
dbt docs serve
```

### Option 3 : PowerShell/Terminal

```powershell
# Depuis d:\lab2
cd dbt_project
dbt run --profiles-dir .
```

---

## 📊 DBT Models

### Bronze Layer
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `stg_jobs_raw` | VIEW | ~131K | Lecture brute du CSV |

### Silver Layer
| Model | Type | Rows | Description |
|-------|------|------|-------------|
| `int_jobs_cleaned` | TABLE | ~131K | Nettoyage texte + dates |
| `int_job_title_normalization` | TABLE | ~100K | Normalisation postes |
| `int_skills_extraction` | TABLE | ~500K | Extraction compétences |

### Gold Layer - Dimensions
| Model | Type | Rows | Keys |
|-------|------|------|------|
| `dim_time` | TABLE | ~2K | date_id (PK) |
| `dim_company` | TABLE | ~5K | company_id (PK) |
| `dim_location` | TABLE | ~3K | location_id (PK) |
| `dim_skills` | TABLE | ~30 | skill_id (PK) |

### Gold Layer - Facts
| Model | Type | Rows | Keys |
|-------|------|------|------|
| `fact_job_offers` | TABLE | ~100K | job_offer_id (SK), Foreign Keys |
| `fact_job_skills` | TABLE | ~500K | job_skill_id (SK), Foreign Keys |

### Gold Layer - Aggregates
| Model | Type | Purpose |
|-------|------|---------|
| `agg_job_offers_by_category_time` | TABLE | Agrégation temporelle |
| `agg_skills_demand` | TABLE | Demande de compétences |
| `agg_location_analysis` | TABLE | Analyse géographique |

---

## 📈 Power BI

### Import des Données

1. **Ouvrir Power BI Desktop**
2. **File → Open → New**
3. **Get Data → Text/CSV**
4. **Charger dans cet ordre** :
   - dim_time.csv
   - dim_company.csv
   - dim_location.csv
   - dim_skills.csv
   - fact_job_offers.csv
   - fact_job_skills.csv

### Créer les Relationships

| From | To | Cardinality |
|------|----|----|
| fact_job_offers[company_id] | dim_company[company_id] | Many:One |
| fact_job_offers[location_id] | dim_location[location_id] | Many:One |
| fact_job_offers[published_date_id] | dim_time[date_id] | Many:One |
| fact_job_skills[job_offer_id] | fact_job_offers[job_offer_id] | Many:One |
| fact_job_skills[skill_id] | dim_skills[skill_id] | Many:One |

### Dashboards à Créer

- **📊 Overview** : KPIs, trends, distributions
- **💼 Job Categories** : Détail par catégorie
- **🔧 Skills** : Top 20, tendances
- **🌍 Geography** : Cartes, villes, pays
- **🏢 Companies** : Top hirers
- **📊 Advanced** : Heatmaps, correlations

Voir [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md) pour le guide complet.

---

## 📚 Documentation

### Fichiers Importants

1. **[ARCHITECTURE.md](ARCHITECTURE.md)**
   - Architecture complète
   - Description détaillée de chaque layer
   - Schema en étoile
   - KPIs définis

2. **[POWER_BI_GUIDE.md](POWER_BI_GUIDE.md)**
   - Configuration Power BI
   - Mesures DAX
   - Design des dashboards
   - Troubleshooting

3. **[run_pipeline.py](run_pipeline.py)**
   - Script d'orchestration
   - Automatisation complète
   - Export CSV

---

## 🔍 Exploratory Queries

### Vérifier les données Silver

```sql
-- DuckDB Console
SELECT COUNT(*) as total_jobs FROM silver.int_job_title_normalization;

SELECT 
    job_category,
    COUNT(*) as count
FROM silver.int_job_title_normalization
GROUP BY job_category
ORDER BY count DESC;

SELECT 
    skill_name,
    COUNT(*) as count
FROM silver.int_skills_extraction
GROUP BY skill_name
ORDER BY count DESC
LIMIT 20;
```

### Vérifier les données Gold

```sql
SELECT COUNT(*) FROM gold.fact_job_offers;
SELECT COUNT(*) FROM gold.dim_company;
SELECT COUNT(*) FROM gold.dim_location;
SELECT COUNT(*) FROM gold.dim_skills;
```

---

## 📊 Quelques Insights Préliminaires

**À découvrir via le dashboard** :

- 📍 Quels pays/villes ont le plus d'offres ?
- 🔧 Quelles sont les top 10 compétences demandées ?
- 💼 Distribution des rôles (Data Engineer vs Scientist vs Analyst) ?
- 🌐 Quel % des postes est en remote ?
- 📈 Quelle est la tendance temporelle des offres ?
- 🏢 Quelles entreprises recrutent le plus ?

---

## 🛠️ Maintenance

### Mise à jour des données

```bash
# Remplacer final_data.csv par une version plus récente
# Puis exécuter :
python run_pipeline.py
```

### Ajouter une nouvelle compétence

Modifier `models/silver/int_skills_extraction.sql` et ajouter :
```sql
UNION ALL SELECT 'New Skill', 'pattern_regex'
```

### Modifier une normalisation

Éditer `models/silver/int_job_title_normalization.sql` :
```sql
WHEN job_title_cleaned LIKE '%pattern%' THEN 'Normalized Name'
```

---

## 📋 Checklist d'Utilisation

- [ ] Installer les dépendances
- [ ] Vérifier `final_data.csv` présent
- [ ] Exécuter `python run_pipeline.py`
- [ ] Vérifier les fichiers CSV dans `data/gold/`
- [ ] Importer en Power BI
- [ ] Créer les relationships
- [ ] Créer les dashboards
- [ ] Paramétrer refresh régulier

---

## 🚀 Prochaines Étapes (Phase 2)

- [ ] **Système de recommandation** : ML model pour matcher offres/profils
- [ ] **API REST** : Servir les recommandations
- [ ] **Alertes** : Notifier des nouvelles offres matchées
- [ ] **Dashboard temps réel** : WebApp avec Streamlit/Dash
- [ ] **Integration LinkedIn** : Scraping automatisé quotidien

---

## 📞 Support

### Erreurs Courantes

**Problème** : `dbt: command not found`
```bash
# Solution
pip install dbt-core dbt-duckdb
```

**Problème** : Import Error DuckDB
```bash
pip install duckdb
```

**Problème** : final_data.csv not found
```bash
# Vérifier le fichier est bien en d:\lab2\
# Ou modifier le chemin dans stg_jobs_raw.sql
```

---

## 📄 Licence

Projet personnel - Usage libre

---

## ✨ Auteur

**Data Engineering & Analytics Project**  
Créé : Janvier 2026  
Version : 1.0

---

**Besoin d'aide ?** Consultez les fichiers de documentation ou les logs DBT en `dbt_project/logs/`.

Happy analyzing! 🚀
