from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import Dht11, Incident, SeuilTemperature
from .serializers import Dht11Serializer, IncidentSerializer

try:
    from .utils import send_telegram
except ImportError:
    def send_telegram(msg): print(f"Simul Telegram: {msg}")


# --- API GET HISTORIQUE (api/) ---
@api_view(['GET'])
def Dlist(request):
    last_records = Dht11.objects.all().order_by('-dt')[:20]
    serializer = Dht11Serializer(last_records, many=True)
    return Response(serializer.data)

# --- API POUR LES GRAPHES (api/data/) ---
@api_view(['GET'])
def data_filtered(request):
    date_str = request.GET.get('date')
    period = request.GET.get('period', 'day')
    
    if date_str:
        try:
            base_date = make_aware(datetime.strptime(date_str, '%Y-%m-%d'))
        except:
            base_date = timezone.now()
    else:
        base_date = timezone.now()

    if period == 'day':
        start_date = base_date.replace(hour=0, minute=0, second=0)
        end_date = base_date.replace(hour=23, minute=59, second=59)
    elif period == 'week':
        start_date = base_date - timedelta(days=7)
        end_date = base_date.replace(hour=23, minute=59, second=59)
    elif period == 'month':
        start_date = base_date - timedelta(days=30)
        end_date = base_date.replace(hour=23, minute=59, second=59)
    else:  # year
        start_date = base_date - timedelta(days=365)
        end_date = base_date.replace(hour=23, minute=59, second=59)

    data = Dht11.objects.filter(dt__range=(start_date, end_date)).order_by('dt')
    serializer = Dht11Serializer(data, many=True)
    return Response(serializer.data)

# --- API POUR LE CAPTEUR (api/post/) ---
class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = Dht11Serializer

    def perform_create(self, serializer):
        instance = serializer.save()

    # ===== Récupération des seuils dynamiques =====
        seuils = SeuilTemperature.objects.order_by('-id').first()
        if not seuils:
            # Crée un seuil par défaut si aucun n'existe
            seuils = SeuilTemperature.objects.create(temp_min=2, temp_max=8)
   
        temp = instance.temp
        is_incident = (temp < seuils.temp_min or temp > seuils.temp_max)

    # ===== Récupération des incidents ouverts =====

        incident = Incident.objects.filter(is_open=True).order_by("-date_traitement").first()

    # ===== Si température en dehors des seuils =====

        if is_incident:
            if not incident:
                send_telegram(f"🚨 NOUVEL INCIDENT : {temp}°C")
                incident = Incident.objects.create(
                    is_open=True,
                    counter=1,
                    max_temp=temp,
                    temp_min_autorisee=seuils.temp_min,
                    temp_max_autorisee=seuils.temp_max
                )
            else:
                incident.counter += 1
                if temp > incident.max_temp:
                    incident.max_temp = temp
                incident.save()

        # ===== Si température normale =====
        else:
            # Fermer tous les incidents ouverts
            if incident:
                incidents_ouverts = Incident.objects.filter(is_open=True)
                for inc in incidents_ouverts:
                    inc.is_open = False
                    inc.ended_at = timezone.now()
                    inc.save()
                send_telegram(f"✅ Retour à la normale : {temp}°C.")

class IncidentStatus(APIView):
    def get(self, request):
        incident = Incident.objects.filter(is_open=True).order_by("-date_traitement").first()
        if not incident:
            return Response({"is_open": False, "counter": 0})
        return Response(IncidentSerializer(incident).data)

class IncidentUpdateOperator(APIView):
    def post(self, request):
        incident = Incident.objects.filter(is_open=True).order_by("-date_traitement").first()
        if not incident:
            return Response(status=400)
        op_num = request.data.get("op")
        ack = request.data.get("ack")
        comment = request.data.get("comment")
        if op_num == 1: 
            incident.op1_ack, incident.op1_comment = ack, comment
        elif op_num == 2: 
            incident.op2_ack, incident.op2_comment = ack, comment
        elif op_num == 3: 
            incident.op3_ack, incident.op3_comment = ack, comment
        incident.save()
        return Response({"status": "updated"})