#models.py
from django.db import models
from django.contrib.auth.models import User



class Dht11(models.Model):
    temp = models.FloatField()
    hum = models.FloatField(default=0)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temp}°C / {self.hum}% - {self.dt}"
    


class OperateurProfile(models.Model):
    """
    Profil opérateur du système IoT.
    L'authentification (login / mot de passe)
    est gérée par le modèle User de Django.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="operator_profile"
    )

    nom = models.CharField(max_length=60)
    prenom = models.CharField(max_length=60)
    telephone = models.CharField(max_length=30)
    email = models.EmailField()
    niveau = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.user.username})"



class Incident(models.Model):
    # === EXISTANT (inchangé) ===
    date_traitement = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)

    max_temp = models.FloatField(default=0)
    counter = models.IntegerField(default=0)

    op1_ack = models.BooleanField(default=False)
    op2_ack = models.BooleanField(default=False)
    op3_ack = models.BooleanField(default=False)

    op1_comment = models.TextField(default="-")
    op2_comment = models.TextField(default="-")
    op3_comment = models.TextField(default="-")

    traite_par = models.CharField(max_length=100, default="Inconnu")
    note_intervention = models.TextField(default="RAS")

    # === ✅ AJOUTS POUR LE NOUVEAU CAHIER DE CHARGE ===

    # Température minimale autorisée
    temp_min_autorisee = models.FloatField(default=2.0)

    # Température maximale autorisée
    temp_max_autorisee = models.FloatField(default=8.0)

    # (optionnel mais très propre) date de sauvegarde des ACK
    op1_saved_at = models.DateTimeField(null=True, blank=True)
    op2_saved_at = models.DateTimeField(null=True, blank=True)
    op3_saved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.date_traitement} - Incident {'OUVERT' if self.is_open else 'FERMÉ'} - Alertes {self.counter}"


# ====== Modif des seuils ======
class SeuilTemperature(models.Model):
    temp_min = models.FloatField(default=2, verbose_name="Température minimale (°C)")
    temp_max = models.FloatField(default=8, verbose_name="Température maximale (°C)")

    def __str__(self):
        return f"Seuils : min {self.temp_min}°C / max {self.temp_max}°C"

    class Meta:
        verbose_name = "Seuil de température"
        verbose_name_plural = "Seuils de température"
