# Guide d'Installation et Démarrage Rapide

## 🚀 Installation Rapide (5 minutes)

### Étape 1 : Créer l'environnement virtuel

```powershell
# Naviguer vers le dossier
cd c:\Users\em\Desktop\projet-jobs\recommendation_system

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\activate
```

### Étape 2 : Installer les dépendances

```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les requirements
pip install -r requirements.txt

# (Optionnel) Télécharger le modèle spaCy français
python -m spacy download fr_core_news_lg
```

### Étape 3 : Premier test

```powershell
# Tester le système (créera les embeddings - 5-10 min la première fois)
python job_recommender.py
```

---

## 🎯 Démarrage Rapide

### Option A : Interface Streamlit (Recommandé pour débuter)

```powershell
# Activer l'environnement
.\venv\Scripts\activate

# Lancer Streamlit
streamlit run app.py
```

Puis ouvrir dans le navigateur : http://localhost:8501

**Fonctionnalités** :
- ✅ Saisie manuelle de profil
- ✅ Upload de CV (PDF, DOCX, TXT)
- ✅ Filtres (localisation, contrat, expérience)
- ✅ Visualisations interactives
- ✅ Export CSV

### Option B : API FastAPI (Pour intégration)

```powershell
# Activer l'environnement
.\venv\Scripts\activate

# Lancer l'API
python api.py
```

Documentation interactive : http://localhost:8000/docs

---

## 📝 Exemples d'Utilisation

### 1. Via l'Interface Streamlit

1. Lancer : `streamlit run app.py`
2. Choisir "Saisie Manuelle" ou "Upload CV"
3. Remplir les champs (profil, compétences, filtres)
4. Cliquer sur "Rechercher"
5. Consulter les résultats dans les 3 onglets

### 2. Via l'API (avec Python)

```python
import requests

# Recommandations depuis profil
url = "http://localhost:8000/api/v1/recommend"
payload = {
    "profile_text": "Data Engineer avec 4 ans d'expérience",
    "keywords": ["Python", "Spark", "AWS", "Databricks"],
    "location_preference": "Paris",
    "contract_type_preference": "Full-time",
    "top_k": 10
}

response = requests.post(url, json=payload)
results = response.json()

# Afficher les recommandations
for rec in results['recommendations']:
    print(f"{rec['title']} - {rec['company']} (Score: {rec['score']})")
```

### 3. Upload de CV via l'API

```python
import requests

url = "http://localhost:8000/api/v1/recommend/cv"

# Uploader le CV
with open("mon_cv.pdf", "rb") as f:
    files = {'cv_file': f}
    params = {
        'keywords': 'Python,SQL,Machine Learning',
        'top_k': 10
    }
    
    response = requests.post(url, files=files, params=params)
    results = response.json()

print(f"Trouvé {results['total_found']} recommandations")
```

### 4. Utilisation Directe en Python

```python
from job_recommender import JobRecommender

# Initialiser (charge les embeddings)
recommender = JobRecommender()

# Recommandations depuis profil
recommendations = recommender.recommend(
    candidate_profile="Machine Learning Engineer, 5 ans d'expérience",
    keywords=['Python', 'TensorFlow', 'PyTorch', 'NLP'],
    location_preference='Remote',
    top_k=10
)

# Afficher
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec['title']} - {rec['company']}")
    print(f"   Score: {rec['score']:.3f}")
    print(f"   Compétences: {', '.join(rec['skills'][:5])}")
    print()
```

---

## 🛠️ Utilisation Avancée

### Changer le Modèle d'Embeddings

Dans `config.py`, modifier :

```python
# Modèle plus rapide
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# OU modèle plus performant
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
```

Puis recréer les embeddings :

```python
from job_recommender import JobRecommender
recommender = JobRecommender(force_reload=True)
```

### Ajuster les Poids de Scoring

Dans `config.py` :

```python
SCORING_WEIGHTS = {
    'semantic_similarity': 0.60,  # Augmenter pour privilégier le sens
    'skills_match': 0.30,         # Augmenter pour privilégier les compétences exactes
    'location_match': 0.05,       # Réduire si localisation moins importante
    'contract_type_match': 0.03,
    'experience_match': 0.02
}
```

### Travailler sur un Échantillon (Tests Rapides)

Dans `job_recommender.py`, méthode `_create_embeddings()` :

```python
# Prendre seulement 10,000 offres pour tests rapides
self.jobs_df = self.preprocessor.preprocess_jobs_df(df_raw, sample_size=10000)
```

---

## 📊 Endpoints API Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Info de l'API |
| `/health` | GET | Statut de santé |
| `/api/v1/recommend` | POST | Recommandation depuis profil |
| `/api/v1/recommend/cv` | POST | Recommandation depuis CV |
| `/api/v1/jobs/{job_id}` | GET | Détails d'une offre |
| `/api/v1/jobs/{job_id}/similar` | GET | Offres similaires |
| `/api/v1/stats` | GET | Statistiques système |

Documentation complète : http://localhost:8000/docs (une fois l'API lancée)

---

## 🐛 Résolution de Problèmes

### Erreur : "ModuleNotFoundError"

```powershell
# Vérifier que l'environnement virtuel est activé
.\venv\Scripts\activate

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur : "Out of memory"

Réduire le nombre d'offres ou utiliser un échantillon (voir section avancée)

### Erreur : "Failed to load model"

Vérifier la connexion internet (téléchargement automatique depuis HuggingFace)

### CV non parsé

- Vérifier le format (PDF, DOCX, TXT supportés)
- Certains PDFs complexes peuvent échouer
- Essayer de convertir en TXT

---

## ⏱️ Temps de Traitement

### Première Exécution
- Création embeddings : **5-10 minutes** (une seule fois)
- Les embeddings sont sauvegardés pour les prochaines fois

### Exécutions Suivantes
- Chargement système : **~10 secondes**
- Recherche : **<100ms par requête**

---

## 💾 Fichiers Générés

Après la première exécution, vous trouverez dans `data/embeddings/` :

- `job_embeddings.npy` (~400MB) : Vecteurs des offres
- `jobs_processed.pkl` (~200MB) : DataFrame préprocessé
- `faiss_index.bin` (~400MB) : Index de recherche

**Total : ~1GB**

---

## 🔄 Mettre à Jour les Données

Si vous modifiez `final_data.csv` :

```python
from job_recommender import JobRecommender

# Forcer le rechargement
recommender = JobRecommender(force_reload=True)
```

---

## 📞 Support

En cas de problème :
1. Vérifier les logs dans la console
2. Consulter la documentation dans README.md
3. Tester avec un échantillon réduit d'abord

Bon développement ! 🚀
