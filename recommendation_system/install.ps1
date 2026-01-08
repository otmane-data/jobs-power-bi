# Script d'installation automatique pour Windows
# Usage: .\install.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation du Système de Recommandation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier Python
Write-Host "1. Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python n'est pas installé!" -ForegroundColor Red
    Write-Host "   Téléchargez Python depuis https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Créer l'environnement virtuel
Write-Host ""
Write-Host "2. Création de l'environnement virtuel..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ! L'environnement existe déjà" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "   ✓ Environnement créé" -ForegroundColor Green
}

# Activer l'environnement
Write-Host ""
Write-Host "3. Activation de l'environnement..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "   ✓ Environnement activé" -ForegroundColor Green

# Mettre à jour pip
Write-Host ""
Write-Host "4. Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ pip mis à jour" -ForegroundColor Green

# Installer les dépendances
Write-Host ""
Write-Host "5. Installation des dépendances (cela peut prendre quelques minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✓ Dépendances installées" -ForegroundColor Green

# Créer les dossiers nécessaires
Write-Host ""
Write-Host "6. Création des dossiers..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\embeddings" | Out-Null
New-Item -ItemType Directory -Force -Path "data\models" | Out-Null
Write-Host "   ✓ Dossiers créés" -ForegroundColor Green

# (Optionnel) Télécharger le modèle spaCy
Write-Host ""
Write-Host "7. Téléchargement du modèle spaCy (optionnel)..." -ForegroundColor Yellow
$installSpacy = Read-Host "   Installer le modèle français ? (o/n)"
if ($installSpacy -eq "o" -or $installSpacy -eq "O") {
    python -m spacy download fr_core_news_lg
    Write-Host "   ✓ Modèle spaCy installé" -ForegroundColor Green
} else {
    Write-Host "   - Ignoré" -ForegroundColor Gray
}

# Résumé
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Installation terminée avec succès!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Yellow
Write-Host "  1. Activer l'environnement: .\venv\Scripts\activate" -ForegroundColor White
Write-Host "  2. Lancer Streamlit: streamlit run app.py" -ForegroundColor White
Write-Host "    OU" -ForegroundColor Gray
Write-Host "  2. Lancer l'API: python api.py" -ForegroundColor White
Write-Host ""
Write-Host "Consultez QUICKSTART.md pour plus d'informations" -ForegroundColor Cyan
Write-Host ""
