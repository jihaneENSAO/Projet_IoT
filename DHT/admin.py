#admin.py
from django.contrib import admin
from .models import Dht11, Incident,OperateurProfile

# Enregistrement du modèle Dht11
@admin.register(Dht11)
class Dht11Admin(admin.ModelAdmin):
    list_display = ('dt', 'temp', 'hum')
    list_filter = ('dt',)
    search_fields = ("dt",)

# Enregistrement du modèle Incident
@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    # Correction des noms de colonnes pour correspondre au modèle
    list_display = (
        "id", 
        "is_open", 
        "date_traitement",  # Remplace start_at
        "ended_at",         # Remplace end_at
        "counter", 
        "max_temp",
        "temp_min_autorisee", 
        "temp_max_autorisee"
    )
    list_filter = ("is_open", "date_traitement")
    search_fields = ("id", "traite_par")

@admin.register(OperateurProfile)
class OperateurProfileAdmin(admin.ModelAdmin):
    list_display = ("niveau", "prenom", "nom", "telephone", "user")
    search_fields = ("nom", "prenom", "telephone", "user__username")
    list_filter = ("niveau",)

# ====== Modif des seuils ======
from .models import SeuilTemperature

@admin.register(SeuilTemperature)
class SeuilTemperatureAdmin(admin.ModelAdmin):
    list_display = ('temp_min', 'temp_max')

# Empêche de créer plusieurs configurations (une seule suffit)
    def has_add_permission(self, request):
        return False if SeuilTemperature.objects.exists() else True