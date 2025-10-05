from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction


from detector.forms import CandidatPlanetaireForm
from .models import CandidatPlanetaire, Prediction
from .utils import predict_disposition

# Create your views here.


@transaction.atomic
def home(request):
    candidates = CandidatPlanetaire.objects.all()

    print("Candidats planétaires récupérés:", candidates)

    if request.method == 'POST':
        # Traiter le formulaire soumis ici
        form = CandidatPlanetaireForm(request.POST)

        print("Formulaire soumis avec les données:", request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()


            predicted_label, probs = predict_disposition(
                koi_period=form.koi_period,
                koi_duration=form.koi_duration,
                koi_depth=form.koi_depth,
                koi_srad=form.koi_srad,
                koi_steff=form.koi_teff,
                koi_slogg=form.koi_slogg,
                koi_impact=form.koi_impact if form.koi_impact is not None else 0,
                is_missing_feature=0
            )

            # Faire la prédiction ici (logique de ML)
            # Pour l'instant, nous allons simuler une prédiction
            prediction = Prediction.objects.create(
                candidat=form,
                confirmed=probs.get('CONFIRMED', 0) * 100,
                candidate=probs.get('CANDIDATE', 0) * 100,
                false_positive=probs.get('FALSE POSITIVE', 0) * 100
            )


            print("Prédiction créée avec les taux de confiance :   ", prediction)
            
            messages.success(request, 'Candidat planétaire soumis avec succès !')

            # Rediriger vers la page des résultats
            return redirect('results', pk=form.pk)
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')

    context = {
        'exoplanets': candidates
    }
    return render(request, 'detector/home.html', context)



def results(request, pk):
    candidat = get_object_or_404(CandidatPlanetaire, pk=pk)
    prediction = getattr(candidat, 'prediction', None)

    print("Candidat planétaire récupéré:", candidat)
    print("Prédiction associée:", prediction)

    # Déterminer la prédiction dominante (celle avec le taux le plus élevé)
    dominant_prediction = None
    if prediction:
        predictions_data = [
            {
                'name': 'CONFIRMED',
                'value': prediction.confirmed,
                'icon': '✅',
                'label_color': 'from-green-500 to-emerald-600',
                'text_color': 'text-green-700',
                'border_color': 'border-green-300',
                'bar_color': 'from-green-400 via-emerald-500 to-green-600',
                'bg_gradient': 'from-green-50 via-emerald-50 to-green-50',
                'border_gradient': 'border-green-500'
            },
            {
                'name': 'CANDIDATE',
                'value': prediction.candidate,
                'icon': '⭐',
                'label_color': 'from-yellow-500 to-amber-600',
                'text_color': 'text-yellow-700',
                'border_color': 'border-yellow-300',
                'bar_color': 'from-yellow-400 via-amber-500 to-yellow-600',
                'bg_gradient': 'from-yellow-50 via-amber-50 to-yellow-50',
                'border_gradient': 'border-yellow-500'
            },
            {
                'name': 'FALSE POSITIVE',
                'value': prediction.false_positive,
                'icon': '❌',
                'label_color': 'from-red-500 to-rose-600',
                'text_color': 'text-red-700',
                'border_color': 'border-red-300',
                'bar_color': 'from-red-400 via-rose-500 to-red-600',
                'bg_gradient': 'from-red-50 via-rose-50 to-red-50',
                'border_gradient': 'border-red-500'
            }
        ]
        
        # Trouver la prédiction avec le taux le plus élevé
        dominant_prediction = max(predictions_data, key=lambda x: x['value'])
        
        print("=" * 50)
        print("ANALYSE DES TAUX DE CONFIANCE")
        print(f"Confirmed: {prediction.confirmed}%")
        print(f"Candidate: {prediction.candidate}%")
        print(f"False Positive: {prediction.false_positive}%")
        print(f"🏆 PRÉDICTION DOMINANTE: {dominant_prediction['name']} avec {dominant_prediction['value']}%")
        print("=" * 50)

    context = {
        'candidat': candidat,
        'prediction': prediction,
        'dominant_prediction': dominant_prediction
    }
    return render(request, 'detector/results.html', context)


def model_info(request):
    """
    Vue pour afficher les informations sur le modèle d'IA
    """
    context = {
        'title': 'Informations sur le Modèle IA'
    }
    return render(request, 'detector/model_info.html', context)
