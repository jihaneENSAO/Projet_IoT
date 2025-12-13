# serializers.py
from rest_framework import serializers
from .models import Dht11

class DHT11serialize(serializers.ModelSerializer):
    # Champ calculé pour l'ISO format
    dt_iso = serializers.SerializerMethodField()

    class Meta:
        model = Dht11
        # Attention ici : tu dois utiliser les noms exacts des champs de ton modèle
        fields = ['temp', 'hum', 'dt_iso']

    def get_dt_iso(self, obj):
        return obj.dt.isoformat()  # 'dt' est ton champ DateTimeField dans le modèle
