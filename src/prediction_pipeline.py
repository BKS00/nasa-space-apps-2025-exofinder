# src/prediction_pipeline.py

import os
import pickle
import numpy as np
import tensorflow as tf
import pandas as pd # Panda est nécessaire pour la manipulation initiale

# --- CONFIGURATION DES CHEMINS D'ACCÈS ---
# Construit un chemin robuste vers le dossier 'artefacts', peu importe d'où le script est appelé.
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # __file__ n'existe pas dans les environnements interactifs comme Colab, on utilise le répertoire de travail.
    BASE_DIR = os.getcwd()

ARTEFACTS_PATH = os.path.join(BASE_DIR, '..', 'artefacts')

# --- CHARGEMENT DES ARTEFACTS AU DÉMARRAGE ---
# Cette section s'exécute une seule fois lorsque le module est importé pour la première fois.
print("Chargement des artefacts du pipeline de prédiction...")
try:
    SCALER = pickle.load(open(os.path.join(ARTEFACTS_PATH, 'data_scaler.pkl'), 'rb'))
    LABEL_ENCODER = pickle.load(open(os.path.join(ARTEFACTS_PATH, 'label_encoder.pkl'), 'rb'))
    MODEL = tf.keras.models.load_model(os.path.join(ARTEFACTS_PATH, 'exofinder_mlp_model.keras'))
    print("--> Artefacts chargés avec succès.")
except Exception as e:
    print(f"ERREUR CRITIQUE : Impossible de charger les artefacts du modèle depuis '{ARTEFACTS_PATH}'. Erreur : {e}")
    SCALER, LABEL_ENCODER, MODEL = None, None, None

# --- LA FONCTION DE PRÉDICTION FINALE (LA "BOÎTE NOIRE") ---

def make_prediction(input_data: dict) -> dict:
    """
    Prend les données d'entrée brutes sous forme de dictionnaire, applique le pipeline complet
    de prétraitement et de modélisation, et renvoie une prédiction formatée.

    Args:
        input_data (dict): Un dictionnaire contenant les 7 caractéristiques physiques de l'interface utilisateur.
                           Ex: {'koi_period': 9.48, 'koi_duration': 2.95, ...}

    Returns:
        dict: Un dictionnaire contenant la prédiction et le score de confiance, ou un message d'erreur.
    """
    if not all([MODEL, SCALER, LABEL_ENCODER]):
        return {"error": "Pipeline de prédiction non initialisé en raison d'une erreur de chargement."}

    try:
        # 1. Validation des entrées (étape de robustesse)
        required_keys = {'koi_period', 'koi_duration', 'koi_depth', 'koi_impact', 'koi_srad', 'koi_slogg', 'koi_steff'}
        if not required_keys.issubset(input_data.keys()):
            missing_keys = required_keys - input_data.keys()
            return {"error": f"Données d'entrée manquantes. Clés requises : {missing_keys}"}

        # 2. Ingénierie de Caractéristiques (recréer le même environnement que pour l'entraînement)
        # Création d'un DataFrame d'une seule ligne
        df = pd.DataFrame([input_data])
        
        # Transformations logarithmiques
        for col in ['koi_period', 'koi_duration', 'koi_depth', 'koi_srad']:
            df[f'{col}_log'] = np.log1p(df[col])
        
        # Ajout du drapeau de données manquantes (il sera toujours 0 pour une entrée de l'UI)
        df['is_missing_feature'] = 0

        # 3. Sélection et Ordonnancement des Caractéristiques Finales
        # L'ordre doit être EXACTEMENT le même que celui utilisé pour entraîner le scaler et le modèle.
        final_features_ordered = [
            'koi_steff', 'koi_slogg', 'koi_period_log', 'koi_duration_log',
            'koi_depth_log', 'koi_srad_log', 'koi_impact', 'is_missing_feature'
        ]
        X = df[final_features_ordered]

        # 4. Standardisation (Scaling)
        X_scaled = SCALER.transform(X)

        # 5. Prédiction avec le Modèle
        probabilities = MODEL.predict(X_scaled)[0]
        
        # 6. Décodage et Formatage de la Sortie
        predicted_index = np.argmax(probabilities)
        confidence = float(probabilities[predicted_index])
        predicted_label = LABEL_ENCODER.inverse_transform([predicted_index])[0]

        return {
            "prediction": predicted_label,
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        # Retourner une erreur propre en cas de problème inattendu
        return {"error": f"Une erreur interne est survenue lors de la prédiction : {e}"}
