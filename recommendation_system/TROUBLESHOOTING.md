# 🔧 Guide de Dépannage - Installation

## Problème Résolu : Erreur d'Installation Pandas

### ❌ Erreur Rencontrée

```
error: subprocess-exited-with-error
× Preparing metadata (pyproject.toml) did not run successfully.
```

**Cause** : Tentative de compiler pandas depuis les sources (tar.gz) sur Windows sans outils de build C++.

### ✅ Solution Appliquée

J'ai mis à jour `requirements.txt` pour utiliser des **versions flexibles** (avec `>=`) qui installent automatiquement les dernières versions avec wheels pré-compilées.

**Changement** :
```diff
- pandas==2.1.4          # Nécessite compilation
+ pandas>=2.0.0          # Utilise wheels Windows
```

---

## 🚀 Installation Corrigée

### Commandes à Exécuter

```powershell
# 1. S'assurer que pip est à jour
pip install --upgrade pip

# 2. Installer les dépendances (version corrigée)
pip install -r requirements.txt

# L'installation prend ~2-5 minutes
# Les packages suivants seront installés :
# - pandas, numpy, scikit-learn (data science)
# - sentence-transformers, transformers (NLP)
# - faiss-cpu (recherche vectorielle)
# - fastapi, uvicorn (API)
# - streamlit (interface web)
# - PyPDF2, python-docx, pdfplumber (parsing CV)
```

### Packages Optionnels

```powershell
# Modèle spaCy français (optionnel mais recommandé)
python -m spacy download fr_core_news_lg

# OU modèle anglais si préféré
python -m spacy download en_core_web_lg
```

---

## 🐛 Autres Problèmes Potentiels

### 1. Erreur "Microsoft Visual C++ required"

**Si vous voyez cette erreur** :
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution** : Utiliser la version corrigée de `requirements.txt` (déjà fait ✅)

### 2. Erreur de Timeout

**Si téléchargement lent** :
```powershell
# Augmenter le timeout
pip install --timeout 1000 -r requirements.txt
```

### 3. Erreur de Permissions

**Si "Permission denied"** :
```powershell
# Installer seulement pour l'utilisateur
pip install --user -r requirements.txt
```

### 4. Conflit de Versions

**Si conflit détecté** :
```powershell
# Créer un nouvel environnement virtuel propre
deactivate
rm -r .venv
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Problème avec FAISS

**Si FAISS échoue à installer** :
```powershell
# Installer une version spécifique
pip install faiss-cpu==1.7.4

# OU si persiste, utiliser conda (si disponible)
conda install -c conda-forge faiss-cpu
```

---

## ✅ Vérification Installation

### Test Rapide

```powershell
# Vérifier que les imports fonctionnent
python -c "import pandas; import numpy; import sentence_transformers; import faiss; print('✅ Installation réussie!')"
```

### Test Complet

```python
# Créer un fichier test_install.py
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np

print("✅ Tous les imports fonctionnent!")

# Tester Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['test'])
print(f"✅ Sentence-BERT OK : {embeddings.shape}")

# Tester FAISS
index = faiss.IndexFlatL2(384)
print("✅ FAISS OK")

print("\n🎉 Installation complète et fonctionnelle!")
```

```powershell
# Exécuter le test
python test_install.py
```

---

## 📦 Si Tout Échoue : Installation Minimale

Si vous rencontrez des difficultés persistantes, voici une **version minimale** pour démarrer :

```txt
# requirements_minimal.txt
sentence-transformers
faiss-cpu
pandas
numpy
fastapi
uvicorn
streamlit
PyPDF2
```

```powershell
pip install -r requirements_minimal.txt
```

**Note** : Certaines fonctionnalités avancées pourront ne pas marcher, mais le système de base fonctionnera.

---

## 🔍 Diagnostic

### Vérifier la Version Python

```powershell
python --version
# Requis : Python 3.8 à 3.11 (3.12+ peut avoir des incompatibilités)
```

### Vérifier l'Environnement Virtuel

```powershell
# S'assurer que le venv est activé
which python  # Linux/Mac
Get-Command python  # Windows PowerShell

# Doit pointer vers .venv/Scripts/python.exe
```

### Lister les Packages Installés

```powershell
pip list
```

---

## 💡 Conseils

1. **Toujours utiliser un environnement virtuel** - Évite les conflits
2. **Mettre à jour pip régulièrement** - `pip install --upgrade pip`
3. **Vérifier la compatibilité Python** - Certains packages ne supportent pas Python 3.12+
4. **Si bloqué** - Supprimer `.venv` et recommencer

---

## 🆘 Support

Si problème persiste après avoir essayé ces solutions :

1. Vérifier les logs d'erreur complets
2. Chercher l'erreur spécifique sur Stack Overflow
3. Utiliser `requirements_minimal.txt` en attendant
4. Considérer l'utilisation de Conda au lieu de pip

---

## ✅ Statut Actuel

- ✅ `requirements.txt` corrigé avec versions flexibles
- 🔄 Installation des dépendances en cours...
- ⏳ Temps estimé : 2-5 minutes

Une fois l'installation terminée, vous pourrez lancer :

```powershell
# Test rapide du système
python job_recommender.py

# OU lancer l'interface
streamlit run app.py
```

Bonne chance ! 🚀
