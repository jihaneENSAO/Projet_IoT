from rest_framework import serializers
from .models import Dht11, Incident

class Dht11Serializer(serializers.ModelSerializer):
    dt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Dht11
        fields = '__all__'

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'