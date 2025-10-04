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

**3. Exemple d'Utilisation dans l'Application Web (Flask/FastAPI)**

```python
# Dans le fichier de votre application web (ex: app.py)
from src.prediction_pipeline import make_prediction

# ... (code de votre route Flask/FastAPI)
@app.route('/predict', methods=['POST'])
def predict():
    # 1. Récupérer les données du formulaire web
    input_data = request.get_json()

    # 2. Appeler notre pipeline de prédiction
    result = make_prediction(input_data)

    # 3. Renvoyer le résultat au frontend
    return jsonify(result)
```
