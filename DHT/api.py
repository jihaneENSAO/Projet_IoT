from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .utils import send_telegram

@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})


# -------- API CREATE --------
class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        if temp > 25:
            # --- Email (facultatif)
            try:
                send_mail(
                    subject="⚠️ Alerte Température élevée",
                    message=f"La température a atteint {temp:.1f} °C à {instance.dt}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=["jihane.bouras.ensao@ump.ac.ma"],
                    fail_silently=True,
                )
            except Exception:
                pass

            # --- Telegram alert
            msg = f"⚠️ Alerte DHT11: {temp:.1f} °C (>25) à {instance.dt}"
            send_telegram(msg)


# -------- API LAST VALUE --------
def latest_json(request):
    obj = Dht11.objects.last()
    return JsonResponse({
        "temperature": obj.temp,
        "humidity": obj.hum,
        "timestamp": obj.dt.isoformat()
    })
