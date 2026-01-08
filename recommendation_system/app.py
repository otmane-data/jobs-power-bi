"""
Application Streamlit pour le système de recommandation d'offres d'emploi
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from job_recommender import JobRecommender
from cv_parser import CVParser

# Configuration de la page
st.set_page_config(
    page_title="Job Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .job-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .score-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
    }
    .skill-tag {
        background-color: #e0e0e0;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser le recommender (avec cache)
@st.cache_resource
def load_recommender():
    """Charge le recommender (mis en cache)"""
    with st.spinner("Chargement du système de recommandation..."):
        return JobRecommender()

# Fonction pour afficher une offre
def display_job_card(job, rank):
    """Affiche une carte d'offre d'emploi"""
    st.markdown(f"""
    <div class="job-card">
        <h3>{rank}. {job['title']}</h3>
        <p><strong>{job['company']}</strong> | {job['location']} | {job['contract_type']}</p>
        <p><span class="score-badge">Score: {job['score']:.3f}</span></p>
        <p><strong>Compétences matchées:</strong> {job['skills_match_count']} / Ratio: {job['skills_match_ratio']:.2%}</p>
        <p><strong>Compétences requises :</strong></p>
        <p>{''.join([f'<span class="skill-tag">{skill}</span>' for skill in job['skills'][:10]])}</p>
        <details>
            <summary><strong>Aperçu de la description</strong></summary>
            <p style="margin-top: 1rem;">{job['description_preview']}</p>
        </details>
        <p style="margin-top: 1rem;">
            <a href="{job['job_url']}" target="_blank" style="text-decoration: none;">
                Voir l'offre complète
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Job Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Système de recommandation pour les métiers de la Data</div>', unsafe_allow_html=True)

# Charger le recommender
try:
    recommender = load_recommender()
    st.success(f"Système chargé : {len(recommender.jobs_df):,} offres disponibles")
except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")
    st.stop()

# Sidebar - Options de recherche
st.sidebar.header("Paramètres de Recherche")

# Mode de saisie
search_mode = st.sidebar.radio(
    "Mode de recherche",
    ["Saisie Manuelle", "Upload de CV"]
)

# Variables pour stocker les inputs
profile_text = ""
keywords_list = []
cv_uploaded = False

if search_mode == "Saisie Manuelle":
    st.sidebar.subheader("Profil Candidat")
    
    profile_text = st.sidebar.text_area(
        "Décrivez votre profil",
        height=150,
        placeholder="Ex: Data Scientist avec 3 ans d'expérience en Machine Learning, Python, et SQL. Recherche poste en région parisienne..."
    )
    
    keywords_input = st.sidebar.text_input(
        "Compétences (séparées par des virgules)",
        placeholder="Python, Machine Learning, SQL, TensorFlow..."
    )
    
    if keywords_input:
        keywords_list = [k.strip() for k in keywords_input.split(',') if k.strip()]

else:  # Upload CV
    st.sidebar.subheader("Upload de CV")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choisir un fichier",
        type=['pdf', 'docx', 'txt'],
        help="Formats supportés: PDF, DOCX, TXT"
    )
    
    if uploaded_file:
        cv_uploaded = True
        
        keywords_input = st.sidebar.text_input(
            "Compétences additionnelles (optionnel)",
            placeholder="Python, SQL..."
        )
        
        if keywords_input:
            keywords_list = [k.strip() for k in keywords_input.split(',') if k.strip()]

# Filtres additionnels
st.sidebar.subheader("Filtres")

location_pref = st.sidebar.text_input(
    "Localisation préférée",
    placeholder="Ex: Paris, Remote, Lyon..."
)

contract_type_pref = st.sidebar.selectbox(
    "Type de contrat",
    ["Tous", "Full-time", "Part-time", "Contract", "Internship"]
)

experience_level = st.sidebar.selectbox(
    "Niveau d'expérience",
    ["Non spécifié", "junior", "mid", "senior", "manager"]
)

top_k = st.sidebar.slider(
    "Nombre de recommandations",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

min_score = st.sidebar.slider(
    "Score minimum",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05
)

# Bouton de recherche
search_button = st.sidebar.button("Rechercher", type="primary", use_container_width=True)

# Zone principale
if search_button:
    # Vérifier les inputs
    if search_mode == "Saisie Manuelle" and not profile_text and not keywords_list:
        st.warning("Veuillez saisir un profil ou des compétences")
        st.stop()
    
    if search_mode == "Upload de CV" and not cv_uploaded:
        st.warning("Veuillez uploader un CV")
        st.stop()
    
    # Lancer la recherche
    with st.spinner("Recherche en cours..."):
        try:
            # Préparer les paramètres
            contract_type = None if contract_type_pref == "Tous" else contract_type_pref
            exp_level = None if experience_level == "Non spécifié" else experience_level
            
            if search_mode == "Saisie Manuelle":
                # Recommandation depuis profil manuel
                recommendations = recommender.recommend(
                    candidate_profile=profile_text,
                    keywords=keywords_list if keywords_list else None,
                    location_preference=location_pref if location_pref else None,
                    contract_type_preference=contract_type,
                    experience_level=exp_level,
                    top_k=top_k,
                    min_score=min_score
                )
            else:
                # Recommandation depuis CV
                cv_bytes = uploaded_file.read()
                recommendations = recommender.recommend_from_cv_bytes(
                    cv_bytes=cv_bytes,
                    cv_filename=uploaded_file.name,
                    additional_keywords=keywords_list if keywords_list else None,
                    location_preference=location_pref if location_pref else None,
                    contract_type_preference=contract_type,
                    experience_level=exp_level,
                    top_k=top_k,
                    min_score=min_score
                )
            
            # Afficher les résultats
            if recommendations:
                st.success(f"{len(recommendations)} offres recommandées")
                
                # Tabs pour différentes vues
                tab1, tab2, tab3 = st.tabs(["Liste", "Tableau", "Statistiques"])
                
                with tab1:
                    # Afficher les cartes d'offres
                    for i, job in enumerate(recommendations, 1):
                        display_job_card(job, i)
                
                with tab2:
                    # Afficher un tableau
                    df_results = pd.DataFrame([{
                        'Rang': i,
                        'Titre': job['title'],
                        'Entreprise': job['company'],
                        'Localisation': job['location'],
                        'Contrat': job['contract_type'],
                        'Score': f"{job['score']:.3f}",
                        'Compétences Matchées': job['skills_match_count'],
                        'URL': job['job_url']
                    } for i, job in enumerate(recommendations, 1)])
                    
                    st.dataframe(
                        df_results,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "URL": st.column_config.LinkColumn("Lien", display_text="Voir")
                        }
                    )
                    
                    # Bouton de téléchargement CSV
                    csv = df_results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Télécharger les résultats (CSV)",
                        data=csv,
                        file_name="recommendations.csv",
                        mime="text/csv"
                    )
                
                with tab3:
                    # Statistiques des recommandations
                    st.subheader("Analyse des Recommandations")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Score Moyen", f"{sum(r['score'] for r in recommendations) / len(recommendations):.3f}")
                    
                    with col2:
                        avg_skills = sum(r['skills_match_count'] for r in recommendations) / len(recommendations)
                        st.metric("Compétences Moyennes Matchées", f"{avg_skills:.1f}")
                    
                    with col3:
                        unique_companies = len(set(r['company'] for r in recommendations))
                        st.metric("Entreprises Uniques", unique_companies)
                    
                    # Distribution des localisations
                    st.subheader("Répartition Géographique")
                    location_counts = pd.Series([r['location'] for r in recommendations]).value_counts()
                    st.bar_chart(location_counts)
                    
                    # Top compétences
                    st.subheader("Compétences les Plus Demandées")
                    all_skills = []
                    for r in recommendations:
                        all_skills.extend(r['skills'])
                    
                    if all_skills:
                        from collections import Counter
                        skill_counts = Counter(all_skills)
                        top_skills_df = pd.DataFrame(
                            skill_counts.most_common(15),
                            columns=['Compétence', 'Occurrences']
                        )
                        st.bar_chart(top_skills_df.set_index('Compétence'))
            
            else:
                st.warning("Aucune offre trouvée avec ces critères. Essayez d'élargir votre recherche.")
        
        except Exception as e:
            st.error(f"Erreur lors de la recherche : {e}")
            import traceback
            st.code(traceback.format_exc())

else:
    # Affichage initial (sans recherche)
    st.info("Configurez votre profil dans la barre latérale et cliquez sur 'Rechercher'")
    
    # Afficher des statistiques globales
    st.subheader("Statistiques du Système")
    
    stats = recommender.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Offres Totales", f"{stats['total_jobs']:,}")
    
    with col2:
        st.metric("Entreprises", f"{stats['unique_companies']:,}")
    
    with col3:
        st.metric("Localisations", f"{stats['unique_locations']:,}")
    
    with col4:
        st.metric("Compétences Moy/Offre", f"{stats['avg_skills_per_job']:.1f}")
    
    # Top 10 compétences
    st.subheader("Top 10 Compétences Demandées")
    
    top_skills = stats['top_10_skills']
    skills_df = pd.DataFrame(top_skills, columns=['Compétence', 'Nombre d\'offres'])
    
    st.bar_chart(skills_df.set_index('Compétence'))
    
    # Distribution niveau expérience
    st.subheader("Distribution Niveau d'Expérience")
    exp_dist = stats['experience_level_distribution']
    exp_df = pd.DataFrame(list(exp_dist.items()), columns=['Niveau', 'Nombre d\'offres'])
    
    st.bar_chart(exp_df.set_index('Niveau'))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>Job Recommender - Système de recommandation pour les métiers de la Data</p>
    <p>Propulsé par Sentence-BERT, FAISS, et Streamlit</p>
</div>
""", unsafe_allow_html=True)
