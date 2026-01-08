"""
Module de préprocessing des données d'offres d'emploi
"""
import re
from typing import List, Dict, Set
import pandas as pd
import numpy as np
from config import DATA_SKILLS, EXPERIENCE_LEVELS


class JobDataPreprocessor:
    """Préprocesseur pour les offres d'emploi"""
    
    def __init__(self):
        self.data_skills = set([skill.lower() for skill in DATA_SKILLS])
        self.experience_keywords = EXPERIENCE_LEVELS
    
    def load_jobs(self, csv_path: str) -> pd.DataFrame:
        """
        Charge les offres d'emploi depuis le CSV
        
        Args:
            csv_path: Chemin vers le fichier CSV
            
        Returns:
            DataFrame avec les offres
        """
        df = pd.read_csv(csv_path)
        print(f"✓ Chargé {len(df):,} offres d'emploi")
        return df
    
    def clean_text(self, text: str) -> str:
        """
        Nettoie un texte (description, titre, etc.)
        
        Args:
            text: Texte brut
            
        Returns:
            Texte nettoyé
        """
        if pd.isna(text):
            return ""
        
        # Convertir en string
        text = str(text)
        
        # Supprimer les balises HTML
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Supprimer les URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        # Supprimer les emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Supprimer les caractères spéciaux excessifs
        text = re.sub(r'[^\w\s.,!?;:()\-\'/]', ' ', text)
        
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text)
        
        # Supprimer la ponctuation répétée
        text = re.sub(r'([.,!?;:]){2,}', r'\1', text)
        
        return text.strip()
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extrait les compétences techniques d'un texte
        
        Args:
            text: Texte (description de poste ou CV)
            
        Returns:
            Liste des compétences trouvées
        """
        if pd.isna(text):
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        # Recherche de chaque compétence dans le texte
        for skill in DATA_SKILLS:
            # Utiliser word boundaries pour éviter les faux positifs
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def extract_experience_level(self, text: str) -> str:
        """
        Extrait le niveau d'expérience d'une description
        
        Args:
            text: Texte de la description
            
        Returns:
            Niveau d'expérience ('junior', 'mid', 'senior', 'manager', 'unknown')
        """
        if pd.isna(text):
            return 'unknown'
        
        text_lower = text.lower()
        
        # Vérifier chaque niveau
        for level, keywords in self.experience_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return 'unknown'
    
    def extract_years_experience(self, text: str) -> int:
        """
        Extrait le nombre d'années d'expérience requis
        
        Args:
            text: Texte de la description
            
        Returns:
            Nombre d'années (0 si non trouvé)
        """
        if pd.isna(text):
            return 0
        
        # Patterns pour trouver "X years", "X+ years", "X-Y years"
        patterns = [
            r'(\d+)\+?\s*(?:years?|ans)',
            r'(\d+)\s*-\s*\d+\s*(?:years?|ans)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass
        
        return 0
    
    def create_job_text(self, row: pd.Series) -> str:
        """
        Crée un texte combiné pour une offre (titre + description)
        
        Args:
            row: Ligne du DataFrame
            
        Returns:
            Texte combiné et nettoyé
        """
        title = self.clean_text(row.get('title', ''))
        description = self.clean_text(row.get('description', ''))
        
        # Donner plus de poids au titre en le répétant
        combined = f"{title}. {title}. {description}"
        
        return combined
    
    def preprocess_jobs_df(self, df: pd.DataFrame, sample_size: int = None) -> pd.DataFrame:
        """
        Préprocesse tout le DataFrame d'offres
        
        Args:
            df: DataFrame brut
            sample_size: Si spécifié, prendre seulement un échantillon (pour tests)
            
        Returns:
            DataFrame préprocessé avec colonnes additionnelles
        """
        print("🔄 Préprocessing des offres d'emploi...")
        
        # Prendre un échantillon si demandé
        if sample_size and sample_size < len(df):
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"  → Échantillon de {sample_size} offres")
        
        # Créer une copie
        df_processed = df.copy()
        
        # Nettoyer les colonnes de texte
        df_processed['title_clean'] = df_processed['title'].apply(self.clean_text)
        df_processed['description_clean'] = df_processed['description'].apply(self.clean_text)
        
        # Créer le texte combiné pour l'embedding
        print("  → Création des textes combinés...")
        df_processed['combined_text'] = df_processed.apply(self.create_job_text, axis=1)
        
        # Extraire les compétences
        print("  → Extraction des compétences...")
        df_processed['skills'] = df_processed['description_clean'].apply(self.extract_skills)
        df_processed['num_skills'] = df_processed['skills'].apply(len)
        
        # Extraire le niveau d'expérience
        print("  → Extraction du niveau d'expérience...")
        df_processed['experience_level'] = df_processed['description_clean'].apply(
            self.extract_experience_level
        )
        df_processed['years_experience'] = df_processed['description_clean'].apply(
            self.extract_years_experience
        )
        
        # Nettoyer la localisation
        df_processed['location_clean'] = df_processed['location'].fillna('Remote').apply(
            lambda x: x.strip() if isinstance(x, str) else 'Remote'
        )
        
        # Nettoyer le type de contrat
        df_processed['contractType_clean'] = df_processed['contractType'].fillna('Unknown').apply(
            lambda x: x.strip() if isinstance(x, str) else 'Unknown'
        )
        
        # Supprimer les lignes avec texte vide
        df_processed = df_processed[df_processed['combined_text'].str.len() > 50].reset_index(drop=True)
        
        print(f"✓ Préprocessing terminé: {len(df_processed):,} offres valides")
        
        return df_processed
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcule des statistiques sur les offres
        
        Args:
            df: DataFrame préprocessé
            
        Returns:
            Dictionnaire de statistiques
        """
        stats = {
            'total_jobs': len(df),
            'unique_companies': df['companyName'].nunique(),
            'unique_locations': df['location_clean'].nunique(),
            'unique_contract_types': df['contractType_clean'].nunique(),
            'avg_skills_per_job': df['num_skills'].mean(),
            'top_10_skills': self._get_top_skills(df, 10),
            'experience_level_distribution': df['experience_level'].value_counts().to_dict(),
        }
        
        return stats
    
    def _get_top_skills(self, df: pd.DataFrame, top_n: int = 10) -> List[tuple]:
        """Retourne les N compétences les plus demandées"""
        all_skills = []
        for skills_list in df['skills']:
            all_skills.extend(skills_list)
        
        from collections import Counter
        skill_counts = Counter(all_skills)
        
        return skill_counts.most_common(top_n)


def normalize_location(location: str) -> str:
    """
    Normalise une localisation pour le matching
    
    Args:
        location: Localisation brute
        
    Returns:
        Localisation normalisée
    """
    if pd.isna(location):
        return 'remote'
    
    location = location.lower().strip()
    
    # Patterns pour remote
    if any(keyword in location for keyword in ['remote', 'télétravail', 'à distance']):
        return 'remote'
    
    # Extraire la ville principale
    # Ex: "Paris, France" -> "paris"
    location = location.split(',')[0].strip()
    
    return location


if __name__ == "__main__":
    # Test du preprocessor
    from config import JOBS_CSV_PATH
    
    preprocessor = JobDataPreprocessor()
    
    # Charger un échantillon
    df = preprocessor.load_jobs(JOBS_CSV_PATH)
    df_processed = preprocessor.preprocess_jobs_df(df, sample_size=1000)
    
    # Afficher les statistiques
    stats = preprocessor.get_statistics(df_processed)
    
    print("\n" + "=" * 80)
    print("STATISTIQUES DES OFFRES")
    print("=" * 80)
    print(f"Total offres: {stats['total_jobs']:,}")
    print(f"Entreprises uniques: {stats['unique_companies']:,}")
    print(f"Localisations uniques: {stats['unique_locations']:,}")
    print(f"Compétences moyennes par offre: {stats['avg_skills_per_job']:.1f}")
    
    print("\n📊 Top 10 compétences:")
    for skill, count in stats['top_10_skills']:
        print(f"  {skill}: {count:,}")
    
    print("\n📈 Distribution niveau d'expérience:")
    for level, count in stats['experience_level_distribution'].items():
        print(f"  {level}: {count:,}")
