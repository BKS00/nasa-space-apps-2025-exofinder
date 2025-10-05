# ExoFinder 🚀

**Découvrir de Nouveaux Mondes avec une IA Rigoureuse.**

Un projet pour le **NASA Space Apps Challenge 2025**, conçu par l'équipe AGI-ESPACE.

---

### ► Résumé du Projet

ExoFinder est une plateforme web qui exploite un modèle de Deep Learning (Réseau de Neurones) pour accélérer la découverte d'exoplanètes. En analysant les caractéristiques physiques d'un signal issu des archives de la NASA, notre solution le classifie instantanément en "Planète Confirmée", "Candidat" ou "Faux Positif", permettant aux scientifiques de concentrer leurs efforts sur les candidats les plus prometteurs.

### 🎯 Le Défi Adressé

Ce projet répond au défi **"Un monde à part : à la recherche d'exoplanètes grâce à l'IA"**. Il s'attaque au goulot d'étranglement majeur de la recherche exoplanétaire : le tri manuel d'un volume de données massif où plus de 95% des signaux sont des faux positifs.

### ✨ Fonctionnalités Clés

*   **Classification par IA :** Utilise un modèle TensorFlow/Keras entraîné sur les données Kepler pour une classification précise.
*   **Démarche Scientifique :** Le modèle a été sélectionné après une analyse exploratoire rigoureuse et une comparaison objective avec d'autres algorithmes (Régression Logistique, Random Forest).
*   **Interface Web Intuitive :** Une application simple pour soumettre des données et visualiser les résultats.
*   **Pipeline Robuste :** Le code est structuré pour séparer la logique IA de l'application web, garantissant la maintenabilité et la clarté.

### 🛠️ Technologies Utilisées

*   **Langage :** Python
*   **Data Science :** TensorFlow/Keras, Scikit-learn, Pandas, Astroquery
*   **Application Web :** DJANGO/Tailwind CSS/JavaScript
*   **Collaboration :** Git, GitHub, Google Colab

---

###  डेमो Démonstration

*   **▶️ Vidéo de Démonstration :** https://drive.google.com/file/d/1HmL6KZXCdCZ7YfgXUeEpGuv9EgrLNS5L/view?usp=sharing
*   **📄 Présentation (Slides) :** https://docs.google.com/presentation/d/1vdsfOwwm4VKyj-wGPM4kyljarMta-yAN/edit?usp=sharing&ouid=112573468174670630142&rtpof=true&sd=true

---

### 🚀 Démarrage Rapide (Lancer l'Application Localement)

Pour lancer l'application web sur votre machine :

**1. Clonez le dépôt :**
```bash
git clone https://github.com/BKS00/nasa-space-apps-2025-exofinder.git
cd nasa-space-apps-2025-exofinder
```

**2. Installez les dépendances :**
```bash
pip install -r requirements.txt
```

**3. Lancez l'application :**
```bash
# Exemple pour Django
python manage.py runserver
```

**4. Ouvrez votre navigateur** à l'adresse `http://127.0.0.1:5000` (ou le port indiqué).

---

### 🧠 Utiliser le Module d'IA (Pour les Développeurs)

Toute la logique de prédiction est encapsulée dans le script `src/prediction_pipeline.py` et sa fonction `make_prediction()`. C'est la méthode officielle et recommandée pour interagir avec notre modèle.

**Entrée :** Un dictionnaire Python avec 7 clés (`koi_period`, `koi_duration`, etc.).
**Sortie :** Un dictionnaire avec la `prediction` et la `confidence`.

**Exemple d'intégration :**

```python
# Importez la fonction
from src.prediction_pipeline import make_prediction

# Préparez vos données d'entrée
input_data = {
    "koi_period": 9.48, "koi_duration": 2.95, "koi_depth": 615.8,
    "koi_impact": 0.146, "koi_srad": 0.927, "koi_slogg": 4.467, "koi_steff": 5455.0
}

# Obtenez le résultat
result = make_prediction(input_data)
print(result)
# Sortie attendue : {'prediction': 'CONFIRMED', 'confidence': 81.23}```
```
---

### 👥 Notre Équipe (AGI-ESPACE)

*   **Salomon Balemba :** Chef de Projet, Data Scientist
*   **VAN TASI MUTUNDO :** Data Scientist
*   **JEPHTE DUNIA :** Développeur Web

---

### 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
