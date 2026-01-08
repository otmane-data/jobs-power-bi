"""
Système de recommandation d'offres d'emploi basé sur Sentence-BERT et FAISS
"""
import os
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Union
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
from tqdm import tqdm

from config import (
    EMBEDDING_MODEL_NAME, EMBEDDING_DIMENSION, JOBS_CSV_PATH,
    EMBEDDINGS_PATH, JOBS_PROCESSED_PATH, FAISS_INDEX_PATH,
    SCORING_WEIGHTS, DEFAULT_TOP_K, MAX_TOP_K
)
from data_preprocessing import JobDataPreprocessor, normalize_location
from cv_parser import CVParser


class JobRecommender:
    """
    Système de recommandation d'offres d'emploi
    
    Utilise Sentence-BERT pour les embeddings sémantiques
    et FAISS pour la recherche vectorielle rapide
    """
    
    def __init__(self, force_reload: bool = False):
        """
        Initialise le recommender
        
        Args:
            force_reload: Si True, recharge les embeddings même s'ils existent
        """
        self.preprocessor = JobDataPreprocessor()
        self.cv_parser = CVParser()
        
        print("🚀 Initialisation du système de recommandation...")
        
        # Charger le modèle d'embeddings
        print(f"  → Chargement du modèle: {EMBEDDING_MODEL_NAME}")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        
        # Variables pour stocker les données
        self.jobs_df = None
        self.embeddings = None
        self.faiss_index = None
        
        # Charger ou créer les embeddings
        if not force_reload and self._embeddings_exist():
            self._load_embeddings()
        else:
            self._create_embeddings()
        
        print("✓ Système de recommandation prêt!")
    
    def _embeddings_exist(self) -> bool:
        """Vérifie si les embeddings existent déjà"""
        return (
            EMBEDDINGS_PATH.exists() and
            JOBS_PROCESSED_PATH.exists() and
            FAISS_INDEX_PATH.exists()
        )
    
    def _create_embeddings(self):
        """Crée les embeddings pour toutes les offres"""
        print("\n📊 Création des embeddings (cette opération peut prendre quelques minutes)...")
        
        # Charger et préprocesser les données
        df_raw = self.preprocessor.load_jobs(str(JOBS_CSV_PATH))
        self.jobs_df = self.preprocessor.preprocess_jobs_df(df_raw)
        
        # Générer les embeddings
        print(f"  → Vectorisation de {len(self.jobs_df):,} offres...")
        job_texts = self.jobs_df['combined_text'].tolist()
        
        # Encoder par batch pour éviter les problèmes de mémoire
        self.embeddings = self.model.encode(
            job_texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Créer l'index FAISS
        print("  → Construction de l'index FAISS...")
        self._build_faiss_index()
        
        # Sauvegarder
        print("  → Sauvegarde des embeddings...")
        self._save_embeddings()
        
        print("✓ Embeddings créés et sauvegardés")
    
    def _build_faiss_index(self):
        """Construit l'index FAISS pour la recherche rapide"""
        # Normaliser les embeddings pour utiliser la similarité cosinus
        faiss.normalize_L2(self.embeddings)
        
        # Créer un index Flat (exact search) avec similarité cosinus
        self.faiss_index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        self.faiss_index.add(self.embeddings.astype('float32'))
    
    def _save_embeddings(self):
        """Sauvegarde les embeddings et les données"""
        # Sauvegarder les embeddings
        np.save(EMBEDDINGS_PATH, self.embeddings)
        
        # Sauvegarder le DataFrame
        with open(JOBS_PROCESSED_PATH, 'wb') as f:
            pickle.dump(self.jobs_df, f)
        
        # Sauvegarder l'index FAISS
        faiss.write_index(self.faiss_index, str(FAISS_INDEX_PATH))
    
    def _load_embeddings(self):
        """Charge les embeddings sauvegardés"""
        print("  → Chargement des embeddings pré-calculés...")
        
        self.embeddings = np.load(EMBEDDINGS_PATH)
        
        with open(JOBS_PROCESSED_PATH, 'rb') as f:
            self.jobs_df = pickle.load(f)
        
        self.faiss_index = faiss.read_index(str(FAISS_INDEX_PATH))
        
        print(f"  → {len(self.jobs_df):,} offres chargées")
    
    def recommend(
        self,
        candidate_profile: str,
        cv_text: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        location_preference: Optional[str] = None,
        contract_type_preference: Optional[str] = None,
        experience_level: Optional[str] = None,
        top_k: int = DEFAULT_TOP_K,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        Recommande des offres d'emploi pour un profil candidat
        
        Args:
            candidate_profile: Description textuelle du profil (saisie utilisateur)
            cv_text: Texte extrait du CV (optionnel)
            keywords: Liste de mots-clés/compétences (optionnel)
            location_preference: Localisation préférée (optionnel)
            contract_type_preference: Type de contrat préféré (optionnel)
            experience_level: Niveau d'expérience ('junior', 'mid', 'senior', etc.)
            top_k: Nombre de recommandations à retourner
            min_score: Score minimum pour filtrer les résultats
            
        Returns:
            Liste de dictionnaires avec les offres recommandées et leurs scores
        """
        # Construire le texte complet du candidat
        candidate_text = self._build_candidate_text(
            candidate_profile, cv_text, keywords
        )
        
        # Vectoriser le profil candidat
        candidate_embedding = self.model.encode([candidate_text], convert_to_numpy=True)
        faiss.normalize_L2(candidate_embedding)
        
        # Rechercher les K*2 plus proches voisins (on filtrera après)
        search_k = min(top_k * 2, len(self.jobs_df))
        distances, indices = self.faiss_index.search(
            candidate_embedding.astype('float32'),
            search_k
        )
        
        # Extraire les compétences du candidat
        candidate_skills = set(self.preprocessor.extract_skills(candidate_text))
        
        # Calculer les scores finaux pour chaque offre
        recommendations = []
        
        for idx, base_score in zip(indices[0], distances[0]):
            job = self.jobs_df.iloc[idx]
            
            # Calcul du score multi-critères
            final_score = self._calculate_final_score(
                base_score=float(base_score),
                job=job,
                candidate_skills=candidate_skills,
                location_preference=location_preference,
                contract_type_preference=contract_type_preference,
                experience_level=experience_level
            )
            
            # Filtrer par score minimum
            if final_score < min_score:
                continue
            
            # Créer l'objet recommandation
            recommendation = {
                'job_id': int(idx),
                'title': job['title'],
                'company': job['companyName'],
                'location': job['location'],
                'contract_type': job['contractType'],
                'work_type': job.get('workType', 'Unknown'),
                'posted_time': job.get('postedTime', 'Unknown'),
                'job_url': job.get('jobUrl', ''),
                'description_preview': job['description_clean'][:300] + '...',
                'skills': job['skills'],
                'experience_level': job['experience_level'],
                'score': round(final_score, 4),
                'semantic_similarity': round(float(base_score), 4),
                'skills_match_count': len(candidate_skills & set(job['skills'])),
                'skills_match_ratio': self._calculate_skills_match_ratio(
                    candidate_skills, set(job['skills'])
                )
            }
            
            recommendations.append(recommendation)
        
        # Trier par score final
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Retourner top K
        return recommendations[:top_k]
    
    def _build_candidate_text(
        self,
        profile: str,
        cv_text: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> str:
        """Construit le texte complet pour le profil candidat"""
        parts = [profile]
        
        if cv_text:
            parts.append(cv_text)
        
        if keywords:
            # Répéter les keywords pour leur donner plus de poids
            keywords_text = ' '.join(keywords) + ' ' + ' '.join(keywords)
            parts.append(keywords_text)
        
        return ' '.join(parts)
    
    def _calculate_final_score(
        self,
        base_score: float,
        job: pd.Series,
        candidate_skills: set,
        location_preference: Optional[str],
        contract_type_preference: Optional[str],
        experience_level: Optional[str]
    ) -> float:
        """Calcule le score final avec pondération multi-critères"""
        
        # Score sémantique (déjà normalisé entre 0 et 1)
        semantic_score = base_score
        
        # Score de matching des compétences
        skills_score = self._calculate_skills_match_ratio(
            candidate_skills, set(job['skills'])
        )
        
        # Score de localisation
        location_score = 1.0
        if location_preference:
            location_norm = normalize_location(location_preference)
            job_location_norm = normalize_location(job['location_clean'])
            location_score = 1.0 if location_norm == job_location_norm else 0.3
        
        # Score de type de contrat
        contract_score = 1.0
        if contract_type_preference:
            contract_score = 1.0 if contract_type_preference.lower() in job['contractType_clean'].lower() else 0.5
        
        # Score d'expérience
        experience_score = 1.0
        if experience_level:
            experience_score = 1.0 if experience_level == job['experience_level'] else 0.7
        
        # Calcul du score final pondéré
        final_score = (
            SCORING_WEIGHTS['semantic_similarity'] * semantic_score +
            SCORING_WEIGHTS['skills_match'] * skills_score +
            SCORING_WEIGHTS['location_match'] * location_score +
            SCORING_WEIGHTS['contract_type_match'] * contract_score +
            SCORING_WEIGHTS['experience_match'] * experience_score
        )
        
        return final_score
    
    def _calculate_skills_match_ratio(self, candidate_skills: set, job_skills: set) -> float:
        """Calcule le ratio de correspondance des compétences"""
        if not candidate_skills or not job_skills:
            return 0.0
        
        intersection = len(candidate_skills & job_skills)
        union = len(candidate_skills | job_skills)
        
        # Jaccard similarity
        return intersection / union if union > 0 else 0.0
    
    def recommend_from_cv_file(
        self,
        cv_path: str,
        additional_keywords: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Recommande des offres depuis un fichier CV
        
        Args:
            cv_path: Chemin vers le fichier CV
            additional_keywords: Mots-clés additionnels
            **kwargs: Autres arguments pour recommend()
            
        Returns:
            Liste de recommandations
        """
        # Parser le CV
        cv_text = self.cv_parser.parse_cv(cv_path)
        cv_text = self.cv_parser.clean_text(cv_text)
        
        # Combiner avec les keywords
        all_keywords = additional_keywords or []
        
        return self.recommend(
            candidate_profile="",
            cv_text=cv_text,
            keywords=all_keywords,
            **kwargs
        )
    
    def recommend_from_cv_bytes(
        self,
        cv_bytes: bytes,
        cv_filename: str,
        additional_keywords: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Recommande des offres depuis un CV uploadé (bytes)
        
        Args:
            cv_bytes: Contenu du CV en bytes
            cv_filename: Nom du fichier
            additional_keywords: Mots-clés additionnels
            **kwargs: Autres arguments pour recommend()
            
        Returns:
            Liste de recommandations
        """
        # Parser le CV
        cv_text = self.cv_parser.parse_cv_bytes(cv_bytes, cv_filename)
        cv_text = self.cv_parser.clean_text(cv_text)
        
        all_keywords = additional_keywords or []
        
        return self.recommend(
            candidate_profile="",
            cv_text=cv_text,
            keywords=all_keywords,
            **kwargs
        )
    
    def get_similar_jobs(self, job_id: int, top_k: int = 10) -> List[Dict]:
        """
        Trouve des offres similaires à une offre donnée
        
        Args:
            job_id: ID de l'offre de référence
            top_k: Nombre d'offres similaires à retourner
            
        Returns:
            Liste d'offres similaires
        """
        if job_id >= len(self.embeddings):
            raise ValueError(f"job_id {job_id} invalide (max: {len(self.embeddings)-1})")
        
        # Récupérer l'embedding de l'offre
        job_embedding = self.embeddings[job_id:job_id+1]
        
        # Rechercher les similaires (top_k + 1 car le premier sera l'offre elle-même)
        distances, indices = self.faiss_index.search(
            job_embedding.astype('float32'),
            top_k + 1
        )
        
        # Exclure l'offre elle-même et créer les résultats
        similar_jobs = []
        for idx, score in zip(indices[0][1:], distances[0][1:]):
            job = self.jobs_df.iloc[idx]
            similar_jobs.append({
                'job_id': int(idx),
                'title': job['title'],
                'company': job['companyName'],
                'location': job['location'],
                'similarity_score': round(float(score), 4),
                'skills': job['skills']
            })
        
        return similar_jobs
    
    def get_job_details(self, job_id: int) -> Dict:
        """
        Récupère les détails complets d'une offre
        
        Args:
            job_id: ID de l'offre
            
        Returns:
            Dictionnaire avec tous les détails
        """
        if job_id >= len(self.jobs_df):
            raise ValueError(f"job_id {job_id} invalide")
        
        job = self.jobs_df.iloc[job_id]
        
        return {
            'job_id': int(job_id),
            'title': job['title'],
            'company': job['companyName'],
            'company_url': job.get('companyUrl', ''),
            'location': job['location'],
            'contract_type': job['contractType'],
            'work_type': job.get('workType', ''),
            'posted_time': job.get('postedTime', ''),
            'published_at': job.get('publishedAt', ''),
            'job_url': job.get('jobUrl', ''),
            'description': job['description'],
            'skills': job['skills'],
            'num_skills': job['num_skills'],
            'experience_level': job['experience_level'],
            'years_experience': job['years_experience']
        }
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur les offres"""
        return self.preprocessor.get_statistics(self.jobs_df)


if __name__ == "__main__":
    # Test du recommender
    print("\n" + "="*80)
    print("TEST DU SYSTÈME DE RECOMMANDATION")
    print("="*80)
    
    # Initialiser
    recommender = JobRecommender()
    
    # Exemple de profil candidat
    candidate_profile = """
    Data Scientist avec 3 ans d'expérience en Machine Learning et Python.
    Compétences: Python, scikit-learn, TensorFlow, SQL, Pandas, NumPy.
    Recherche poste en région parisienne, full-time.
    """
    
    keywords = ['Python', 'Machine Learning', 'Data Science', 'SQL', 'TensorFlow']
    
    # Obtenir des recommandations
    print("\n🔍 Recherche de recommandations...")
    recommendations = recommender.recommend(
        candidate_profile=candidate_profile,
        keywords=keywords,
        location_preference="Paris",
        contract_type_preference="Full-time",
        top_k=5
    )
    
    # Afficher les résultats
    print(f"\n📋 Top {len(recommendations)} recommandations:\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} - {rec['company']}")
        print(f"   📍 {rec['location']} | 📄 {rec['contract_type']}")
        print(f"   🎯 Score: {rec['score']:.3f} | Compétences matchées: {rec['skills_match_count']}")
        print(f"   💼 {', '.join(rec['skills'][:5])}...")
        print()
