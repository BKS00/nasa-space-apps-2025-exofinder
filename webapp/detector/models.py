from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.


class CandidatPlanetaire(models.Model):
    # les champs qui décrivent le transit
    koi_period = models.FloatField(_('Période Orbitale (jours)'))
    koi_duration = models.FloatField(_('Durée du Transit (heures)'))
    koi_depth = models.FloatField(_('Profondeur du Transit (ppm)'))
    koi_impact = models.FloatField(_('Paramètre d\'impact (masse terrestre)'), null=True, blank=True)

    # les champs qui décrivent l'étoile hôte
    koi_teff = models.FloatField(_('Température effective (K)'))
    koi_slogg = models.FloatField(_('Log de la gravité de surface (cgs)'))
    koi_srad = models.FloatField(_('Rayon (rayons solaires)'), null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidats', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Candidat Planétaire')
        verbose_name_plural = _('Candidats Planétaires')

    def __str__(self):
        return f"Candidat {self.id}"


class Prediction(models.Model):
    candidat = models.OneToOneField(CandidatPlanetaire, on_delete=models.CASCADE, related_name='prediction')
    confirmed = models.FloatField(_('Taux de confiance de confirmation (%)'))
    candidate = models.FloatField(_('Taux de confiance de candidat (%)'))
    false_positive = models.FloatField(_('Taux de confiance de faux positif (%)'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Prédiction')
        verbose_name_plural = _('Prédictions')

    def __str__(self):
        return f"Prédiction pour Candidat {self.candidat.id}"