# nasa-space-apps-2025-exofinder
Projet pour le NASA Space Apps Challenge 2025. Un outil d'IA pour détecter les exoplanètes.
* **Notebook Colab Partagé :** https://colab.research.google.com/drive/15P8DN740liWaPegbb0Vwqgt-FiYYsBaa?usp=sharing

---

### **Comment Utiliser le Modèle d'IA**

Le Pôle Web (JEFTE) n'a pas besoin d'interagir directement avec les notebooks ou les fichiers de modèle. Toute la logique de prédiction est encapsulée dans le script `src/prediction_pipeline.py`.

**1. Entrée Requise**

La fonction `make_prediction` attend un dictionnaire Python contenant les **7 caractéristiques physiques** suivantes :
*   `koi_period` (float)
*   `koi_duration` (float)
*   `koi_depth` (float)
*   `koi_impact` (float)
*   `koi_srad` (float)
*   `koi_slogg` (float)
*   `koi_steff` (float)

**2. Sortie Fournie**

La fonction renvoie un dictionnaire contenant la prédiction et un score de confiance.
*   **En cas de succès :** `{'prediction': 'CONFIRMED', 'confidence': 81.23}`
*   **En cas d'erreur :** `{'error': 'Description de l'erreur'}`

**3. Exemple d'Utilisation dans l'Application Web (Django)**

```python
# Dans le fichier utils d'une application Django (ex: utils.py)
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
```
