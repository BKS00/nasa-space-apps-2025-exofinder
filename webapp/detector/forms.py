from django.forms import ModelForm
from .models import CandidatPlanetaire


class CandidatPlanetaireForm(ModelForm):
    class Meta:
        model = CandidatPlanetaire
        fields = ['koi_period', 'koi_duration', 'koi_depth', 'koi_impact', 'koi_teff', 'koi_slogg', 'koi_srad']