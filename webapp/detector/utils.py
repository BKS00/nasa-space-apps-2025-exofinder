import numpy as np
import pickle
from tensorflow.keras.models import load_model
from core.settings import BASE_DIR

# --- CONFIGURATION DES CHEMINS D'ACCÈS ---

SCALER_PATH = f"{BASE_DIR}/static/model/data_scaler.pkl"
ENCODER_PATH = f"{BASE_DIR}/static/model/label_encoder.pkl"
MODEL_PATH = f"{BASE_DIR}/static/model/exofinder_mlp_model.keras"

# --- CHARGEMENT DES ARTEFACTS ---
print("Chargement des artefacts...")
try:
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    with open(ENCODER_PATH, 'rb') as f:
        label_encoder = pickle.load(f)

    model_mlp = load_model(MODEL_PATH)
    print("Artefacts chargés avec succès.")
except FileNotFoundError as e:
    print(f"ERREUR : Fichier non trouvé. {e}")
    print("Veuillez vérifier les chemins d'accès et que votre Drive est bien monté.")
    exit()

# --- FONCTION DE PRÉDICTION ---
# Cette fonction encapsule tout le pipeline de pré-traitement et de prédiction.

def predict_disposition(koi_period, koi_duration, koi_depth, koi_srad,
                          koi_steff, koi_slogg, koi_impact, is_missing_feature):
    """
    Prédit la disposition d'un objet d'intérêt Kepler à partir de ses caractéristiques physiques.

    Args:
        (Les 8 caractéristiques finales utilisées par le modèle)

    Returns:
        str: Le nom de la classe prédite ('CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE').
        dict: Un dictionnaire des probabilités pour chaque classe.
    """
    # 1. Appliquer les transformations logarithmiques
    koi_period_log = np.log1p(koi_period)
    koi_duration_log = np.log1p(koi_duration)
    koi_depth_log = np.log1p(koi_depth)
    koi_srad_log = np.log1p(koi_srad)

    # 2. Créer le vecteur de caractéristiques dans le bon ordre
    features = np.array([[
        koi_steff, koi_slogg,
        koi_period_log, koi_duration_log,
        koi_depth_log, koi_srad_log,
        koi_impact,
        is_missing_feature
    ]])

    # 3. Standardiser les données avec le scaler chargé
    features_scaled = scaler.transform(features)

    # 4. Faire la prédiction
    probabilities = model_mlp.predict(features_scaled)[0]

    # 5. Interpréter les résultats
    predicted_index = np.argmax(probabilities)
    predicted_class_name = label_encoder.inverse_transform([predicted_index])[0]

    class_probabilities = {label: prob for label, prob in zip(label_encoder.classes_, probabilities)}

    return predicted_class_name, class_probabilities

# # --- EXEMPLE D'UTILISATION ---
# # Simule une nouvelle observation.
# # (Exemple basé sur Kepler-664 b, une planète confirmée de votre dataset)
# predicted_label, probs = predict_disposition(
#     koi_period=2.525592,
#     koi_duration=1.65450,
#     koi_depth=603.3,
#     koi_srad=1.046,
#     koi_steff=6031.0,
#     koi_slogg=4.438,
#     koi_impact=0.701,
#     is_missing_feature=0 # Aucune donnée manquante pour cet exemple
# )

# print("\n--- Résultat de la Prédiction ---")
# print(f"Classe Prédite : {predicted_label}")
# print("Probabilités par classe :")
# for label, prob in probs.items():
#     print(f"  - {label}: {prob:.2%}")