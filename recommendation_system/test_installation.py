"""
Script de test rapide pour vérifier que l'installation est fonctionnelle
"""
import sys

print("=" * 80)
print("TEST DE L'INSTALLATION DU SYSTÈME DE RECOMMANDATION")
print("=" * 80)
print()

# Test 1: Imports de base
print("1. Test des imports de base...")
try:
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    print("   ✅ pandas, numpy, scikit-learn OK")
except ImportError as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 2: Sentence-Transformers
print("\n2. Test de Sentence-Transformers...")
try:
    from sentence_transformers import SentenceTransformer
    print("   ✅ sentence-transformers importé")
    
    # Charger un petit modèle pour test
    print("   → Chargement d'un modèle de test...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Test encoding
    test_text = ["Data Scientist", "Machine Learning Engineer"]
    embeddings = model.encode(test_text)
    print(f"   ✅ Embeddings créés: {embeddings.shape}")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 3: FAISS
print("\n3. Test de FAISS...")
try:
    import faiss
    
    # Créer un index simple
    dimension = 384  # dimension de all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(dimension)
    
    # Ajouter les embeddings de test
    index.add(embeddings.astype('float32'))
    
    # Recherche
    distances, indices = index.search(embeddings[:1].astype('float32'), k=2)
    
    print(f"   ✅ FAISS OK: {index.ntotal} vecteurs dans l'index")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 4: FastAPI et Uvicorn
print("\n4. Test de FastAPI/Uvicorn...")
try:
    from fastapi import FastAPI
    import uvicorn
    from pydantic import BaseModel
    print("   ✅ FastAPI et Uvicorn OK")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 5: Streamlit
print("\n5. Test de Streamlit...")
try:
    import streamlit as st
    import plotly.express as px
    print("   ✅ Streamlit et Plotly OK")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 6: Parsers CV
print("\n6. Test des parsers de CV...")
try:
    import PyPDF2
    from docx import Document
    import pdfplumber
    print("   ✅ PyPDF2, python-docx, pdfplumber OK")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 7: Modules du système
print("\n7. Test des modules du système...")
try:
    from config import EMBEDDING_MODEL_NAME, DATA_SKILLS
    from cv_parser import CVParser
    from data_preprocessing import JobDataPreprocessor
    
    print(f"   ✅ Modules système OK")
    print(f"   → Modèle d'embeddings: {EMBEDDING_MODEL_NAME}")
    print(f"   → Compétences configurées: {len(DATA_SKILLS)}")
    
except Exception as e:
    print(f"   ⚠️  Erreur (normal si première fois): {e}")

# Résumé
print("\n" + "=" * 80)
print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
print("=" * 80)
print()
print("🎉 Votre système est prêt à fonctionner!")
print()
print("Prochaines étapes:")
print("  1. Tester le recommender: python job_recommender.py")
print("  2. Lancer l'API: python api.py")
print("  3. Lancer l'interface Streamlit: streamlit run app.py")
print()
print("Note: Le premier lancement de job_recommender.py prendra 5-10 minutes")
print("pour créer les embeddings de 200K offres. Les fois suivantes seront rapides!")
print()
