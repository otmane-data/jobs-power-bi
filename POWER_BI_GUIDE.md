# GUIDE POWER BI - JOB INTELLIGENT

## 📊 Configuration Power BI pour Job Intelligent

### Objectif
Créer un dashboard interactif permettant l'analyse complète des offres d'emploi Data avec système de KPIs et recommandations.

---

## Étape 1 : Importer les Données

### 1.1 Importer les tables Gold

**Dans Power BI Desktop** :

1. Accueil → Obtenir les données → Texte/CSV
2. Naviguer vers : `D:\lab2\data\gold\`
3. Charger les fichiers dans cet ordre :

```
1. dim_time.csv        (Dimension temps)
2. dim_company.csv     (Dimension entreprise)
3. dim_location.csv    (Dimension localisation)
4. dim_skills.csv      (Dimension compétences)
5. fact_job_offers.csv (Table de fait principale)
6. fact_job_skills.csv (Bridge table skills)
7. agg_*.csv           (Tables d'agrégation - optionnel)
```

### 1.2 Transformer les Données

Dans l'éditeur de requête Power Query :

```
- Vérifier les types de colonnes
- Supprimer les colonnes inutiles
- Charger les données
```

---

## Étape 2 : Modèle de Données

### 2.1 Créer les Relations

**Onglet "Modèle"** → Ajouter les relations suivantes :

| Relation | Type | Cardinality |
|----------|------|-------------|
| fact_job_offers[company_id] → dim_company[company_id] | 1:* | Many:One |
| fact_job_offers[location_id] → dim_location[location_id] | 1:* | Many:One |
| fact_job_offers[published_date_id] → dim_time[date_id] | 1:* | Many:One |
| fact_job_skills[job_offer_id] → fact_job_offers[job_offer_id] | 1:* | Many:One |
| fact_job_skills[skill_id] → dim_skills[skill_id] | 1:* | Many:One |

### 2.2 Configuration du Modèle

**Marquer comme table de fait/dimension** :

```
Dimension:
├─ dim_time → Marquer comme dimension
├─ dim_company → Marquer comme dimension
├─ dim_location → Marquer comme dimension
└─ dim_skills → Marquer comme dimension

Faits:
├─ fact_job_offers → Marquer comme faits
└─ fact_job_skills → Marquer comme faits
```

---

## Étape 3 : Mesures et Colonnes Calculées

### 3.1 Mesures Principales

**Dans la table fact_job_offers** :

```dax
-- Total Job Offers
Total Jobs = COUNTA(fact_job_offers[job_offer_id])

-- Total Companies
Total Companies = DISTINCTCOUNT(fact_job_offers[company_id])

-- Total Locations
Total Locations = DISTINCTCOUNT(fact_job_offers[location_id])

-- Total Skills Mentioned
Total Skills = DISTINCTCOUNT(fact_job_skills[skill_id])

-- Remote Percentage
Remote % = 
  DIVIDE(
    SUM(fact_job_offers[is_remote]),
    COUNTA(fact_job_offers[job_offer_id]),
    0
  ) * 100

-- Permanent Percentage
Permanent % =
  DIVIDE(
    SUM(fact_job_offers[is_permanent]),
    COUNTA(fact_job_offers[job_offer_id]),
    0
  ) * 100

-- Average Description Length
Avg Description Length = AVERAGE(fact_job_offers[description_length])

-- Average Word Count
Avg Word Count = AVERAGE(fact_job_offers[word_count])
```

### 3.2 Mesures par Catégorie

**Ajouter dans fact_job_offers** :

```dax
-- Data Engineer Count
Data Engineer Count = 
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Engineer"
  )

-- Data Scientist Count
Data Scientist Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Scientist"
  )

-- Data Analyst Count
Data Analyst Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Data Analyst"
  )

-- ML Engineer Count
ML Engineer Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "ML Engineer"
  )

-- Analytics Engineer Count
Analytics Engineer Count =
  CALCULATE(
    COUNTA(fact_job_offers[job_offer_id]),
    fact_job_offers[job_category] = "Analytics Engineer"
  )
```

### 3.3 Mesures de Tendance

```dax
-- YoY Growth
YoY Growth % =
  VAR CurrentYear = YEAR(TODAY())
  VAR PreviousYear = CurrentYear - 1
  RETURN
    DIVIDE(
      CALCULATE([Total Jobs], YEAR(fact_job_offers[published_date]) = CurrentYear),
      CALCULATE([Total Jobs], YEAR(fact_job_offers[published_date]) = PreviousYear),
      0
    ) - 1

-- MoM Change
MoM Change =
  VAR CurrentMonth = MONTH(TODAY())
  VAR CurrentYear = YEAR(TODAY())
  RETURN
    CALCULATE(
      [Total Jobs],
      MONTH(fact_job_offers[published_date]) = CurrentMonth,
      YEAR(fact_job_offers[published_date]) = CurrentYear
    )
```

---

## Étape 4 : Dashboards Recommandés

### Dashboard 1 : 📈 Overview

**Visualisations** :

1. **KPI Cards** (4 cartes côte à côte)
   - Total Jobs (grand nombre)
   - Total Companies
   - Total Locations
   - Total Skills
   - % Remote
   - % Permanent

2. **Line Chart** : Trend mensuel
   - Axe X : dim_time[published_year_month]
   - Axe Y : [Total Jobs]
   - Couleur : fact_job_offers[job_category]

3. **Pie Chart** : Distribution par Catégorie
   - Champ : fact_job_offers[job_category]
   - Valeur : [Total Jobs]

4. **Pie Chart** : Distribution par Type de Contrat
   - Champ : fact_job_offers[contract_type]
   - Valeur : [Total Jobs]

5. **Pie Chart** : Distribution par Work Type
   - Champ : fact_job_offers[work_type]
   - Valeur : [Total Jobs]

### Dashboard 2 : 💼 Job Categories

**Visualisations** :

1. **Table Détaillée**
   - Colonnes : job_title, company_name, location, contract_type, work_type
   - Filtre : interactif sur job_category

2. **Stacked Bar Chart** : Contrats par Catégorie
   - Axe X : job_category
   - Axe Y : Count
   - Légende : contract_type

3. **Stacked Bar Chart** : Work Type par Catégorie
   - Axe X : job_category
   - Axe Y : Count
   - Légende : work_type

4. **Scatter Plot** : Description Length vs Word Count
   - Axe X : avg_description_length
   - Axe Y : avg_word_count
   - Couleur : job_category

### Dashboard 3 : 🔧 Skills Analysis

**Visualisations** :

1. **Top 20 Skills Bar Chart**
   - Axe X : dim_skills[skill_name]
   - Axe Y : COUNT(fact_job_skills[skill_id])
   - Tri : descendant
   - Filtre : Top 20

2. **Skills by Category Bar Chart**
   - Axe X : dim_skills[skill_category]
   - Axe Y : COUNT(fact_job_skills[skill_id])

3. **Skill Trend Line**
   - Axe X : dim_time[published_year_month]
   - Axe Y : COUNT(fact_job_skills[skill_id])
   - Couleur : dim_skills[skill_name] (Top 5)

4. **Matrix** : Skills par Job Category
   - Lignes : job_category
   - Colonnes : skill_name (Top 10)
   - Valeurs : COUNT

### Dashboard 4 : 🌍 Geographic Analysis

**Visualisations** :

1. **Map** : Job Offers par Country
   - Localisation : dim_location[country]
   - Couleur : [Total Jobs]

2. **Map** : Job Offers par City (avec drill-down)
   - Localisation : dim_location[city]
   - Couleur : [Total Jobs]

3. **Bar Chart** : Top 20 Cities
   - Axe X : dim_location[city]
   - Axe Y : [Total Jobs]
   - Tri : descendant

4. **Pie Chart** : Remote % par Country
   - Champ : dim_location[country]
   - Valeur : [Remote %]

5. **Table** : Location Metrics
   - Colonnes : location, city, country, count_job_offers, count_companies, pct_remote

### Dashboard 5 : 🏢 Company Analysis

**Visualisations** :

1. **Top 20 Hiring Companies Bar Chart**
   - Axe X : dim_company[company_name]
   - Axe Y : COUNT(fact_job_offers[job_offer_id])
   - Filtre : Top 20

2. **Company Details Table**
   - Colonnes : company_name, location, count_jobs, job_categories, skills_required

3. **Bubble Chart** : Companies
   - Axe X : count_jobs
   - Axe Y : avg_word_count
   - Taille : count_companies
   - Couleur : job_category

### Dashboard 6 : 📊 Advanced Analytics

**Visualisations** :

1. **Histogram** : Distribution de la longueur des descriptions
   - Champ : description_length
   - Bins : 50-100 mots

2. **KPI avec Jauge** : Satisfaction Score
   - Formule personnalisée basée sur critères

3. **Heatmap** : Skills par Location
   - Lignes : dim_location[city]
   - Colonnes : dim_skills[skill_name]
   - Valeurs : COUNT

4. **Temporal Heatmap** : Offres par Jour de la Semaine & Heure
   - Lignes : dim_time[day_name]
   - Colonnes : hour (extrait de postedTime)
   - Valeurs : COUNT

---

## Étape 5 : Filtres et Slicers

**Ajouter les slicers suivants** :

```
📅 Time Slicers:
├─ published_year (All selected by default)
├─ published_month (All)
└─ published_year_month (Timeline)

🏷️ Category Slicers:
├─ job_category (Multi-select)
├─ contract_type (Multi-select)
└─ work_type (Multi-select)

📍 Location Slicers:
├─ country (Dropdown)
└─ city (Dependent on country)

🔧 Skills Slicers:
├─ skill_category (Multi-select)
└─ skill_name (Multi-select with search)

🏢 Company Slicers:
└─ company_name (Dropdown with search)
```

---

## Étape 6 : Interactions entre Pages

**Configurer les interactions** :

```
Slicer: job_category
├─ Overview → Filter
├─ Job Categories → Filter
└─ Skills Analysis → Filter

Slicer: dim_location[country]
├─ Overview → Filter
├─ Geographic Analysis → Filter
└─ Company Analysis → Filter
```

---

## Étape 7 : Mise en Forme

### Color Scheme
```
Job Categories:
- Data Engineer: #1f77b4 (Blue)
- Data Scientist: #ff7f0e (Orange)
- Data Analyst: #2ca02c (Green)
- ML Engineer: #d62728 (Red)
- Analytics Engineer: #9467bd (Purple)
- Other: #7f7f7f (Gray)
```

### Formatting
```
- Nombres : Format avec séparateurs (1,000)
- Pourcentages : 2 décimales
- Dates : DD/MM/YYYY
- Descriptions : Tronquées à 100 caractères
```

---

## Étape 8 : Performance & Optimization

### Tips Power BI
1. **Utiliser des agrégations** pour les grandes tables
2. **Ajouter des filtres implicites** pour réduire les données
3. **Utiliser des tables de cache** pour les calculs complexes
4. **Vérifier les performances** avec Performance Analyzer
5. **Exporter en Excel** si nécessaire pour partage

### Requête d'optimisation
```dax
-- Performance Test
EVALUATE
SUMMARIZECOLUMNS(
    fact_job_offers[job_category],
    dim_time[published_year_month],
    "Total Jobs", COUNTA(fact_job_offers[job_offer_id]),
    "Avg Description", AVERAGE(fact_job_offers[description_length])
)
```

---

## Étape 9 : Publish & Share

### Publier sur Power BI Service

1. **Fichier → Publier**
2. Choisir l'espace de travail
3. Configurer les rafraîchissements
4. Partager avec l'équipe

### Configuration du Refresh
```
Plage horaire : 02:00 - 06:00 UTC
Fréquence : Quotidienne
Notifier : En cas d'erreur
```

---

## KPIs Dashboard Summary

| KPI | Formule | Target |
|-----|---------|--------|
| Total Offers | COUNTA() | Monitor |
| Growth MoM | % Change | +5% |
| Companies | DISTINCTCOUNT() | 3000+ |
| Skills Diversity | DISTINCTCOUNT() | 25+ |
| Remote % | SUM(is_remote) / COUNT() | 30%+ |
| Permanent % | SUM(is_permanent) / COUNT() | 70%+ |

---

## Troubleshooting

### Données manquantes ?
- Vérifier les relations
- Consulter Performance Analyzer
- Valider les données source

### Performances lentes ?
- Réduire les filtres
- Ajouter des agrégations
- Vérifier DirectQuery vs Import

### Calculs incorrects ?
- Vérifier les mesures DAX
- Consulter le contexte de filtre
- Tester avec des valeurs simples

---

**Créé** : 7 janvier 2026  
**Version** : 1.0  
**Pour** : JOB INTELLIGENT Project
