from django.contrib import admin
from .models import CandidatPlanetaire, Prediction
# Register your models here.

@admin.register(CandidatPlanetaire)
class CandidatPlanetaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'koi_period', 'koi_duration', 'koi_depth', 'koi_impact', 'koi_teff', 'koi_slogg', 'koi_srad', 'user')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'candidat', 'confirmed', 'candidate', 'false_positive', 'created_at')
    list_filter = ('candidat__koi_teff', 'candidat__koi_slogg')


