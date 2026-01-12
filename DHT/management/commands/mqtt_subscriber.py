import json
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from DHT.models import Dht11, Incident, SeuilTemperature
import threading

# --- Fonction pour envoyer Gmail de façon asynchrone ---
def send_email_async(subject, message, recipients):
    threading.Thread(
        target=send_mail,
        args=(subject, message, settings.EMAIL_HOST_USER, recipients),
        kwargs={'fail_silently': False}
    ).start()

# --- Importation de send_telegram ---
try:
    from DHT.utils import send_telegram
except ImportError:
    def send_telegram(msg):
        print(f"Simul Telegram: {msg}")

# --- Fonction appelée lors de la connexion au broker MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion au broker MQTT réussie !")
        client.subscribe(settings.MQTT_TOPIC_DHT, qos=1)
    else:
        print(f"Échec de la connexion, code retour : {rc}")

# --- Fonction appelée à chaque message MQTT reçu ---
def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic} : {msg.payload.decode()}")

    try:
        data = json.loads(msg.payload.decode())
        temp = float(data.get("temperature", 0))
        hum = float(data.get("humidity", 0))

        # 1️⃣ Enregistrement de la mesure dans la base
        instance = Dht11.objects.create(temp=temp, hum=hum)
        print(f"Donnée enregistrée : {temp}°C | {hum}%")

        # 2️⃣ Récupération des seuils dynamiques depuis l'admin
        seuils = SeuilTemperature.objects.order_by('-id').first()
        if not seuils:
            seuils = SeuilTemperature.objects.create(temp_min=2, temp_max=8)

        # 3️⃣ Vérification si un incident est nécessaire
        is_incident = (temp < seuils.temp_min or temp > seuils.temp_max)

        # On récupère le dernier incident ouvert
        incident = Incident.objects.filter(is_open=True).order_by("-date_traitement").first()

        if is_incident:
            # 🔴 Cas alerte : créer ou mettre à jour l'incident
            if not incident:
                incident = Incident.objects.create(
                    is_open=True,
                    counter=1,
                    max_temp=temp,
                    temp_min_autorisee=seuils.temp_min,
                    temp_max_autorisee=seuils.temp_max
                )
                msg_telegram = f"🚨 NOUVEL INCIDENT : {temp}°C"
                send_telegram(msg_telegram)
                print("!!! NOUVEL INCIDENT CRÉÉ !!!")

                # --- Envoi Gmail asynchrone ---
                send_email_async(
                    subject=f"🚨 Alerte Température : {temp}°C",
                    message=f"Un nouvel incident a été détecté : {temp}°C.\nSeuils: {seuils.temp_min}-{seuils.temp_max}°C",
                    recipients=["chaimae.elazimani.ensao@ump.ac.ma"]
                )
                print("Mail déclenché pour le nouvel incident.")

            else:
                incident.counter += 1
                if temp > incident.max_temp:
                    incident.max_temp = temp
                incident.save()
                msg_telegram = f"🚨 Incident mis à jour : {temp}°C (Compteur {incident.counter})"
                send_telegram(msg_telegram)
                print(f"Incident mis à jour (Compteur: {incident.counter})")

        else:
            # ✅ Cas normal : fermer tous les incidents ouverts
            open_incidents = Incident.objects.filter(is_open=True)
            for inc in open_incidents:
                inc.is_open = False
                inc.ended_at = timezone.now()
                inc.save()
                msg_telegram = f"✅ Retour à la normale : {temp}°C"
                send_telegram(msg_telegram)
                print("Incident fermé (Retour à la normale)")

                # --- Envoi Gmail asynchrone pour fermeture ---
                send_email_async(
                    subject=f"✅ Retour à la normale : {temp}°C",
                    message=f"L'incident a été résolu. Température actuelle : {temp}°C",
                    recipients=[settings.EMAIL_HOST_USER]
                )
                print("Mail déclenché pour la fermeture d'incident.")

    except json.JSONDecodeError:
        print("Erreur JSON")
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")

# --- Commande Django pour lancer le subscriber MQTT ---
class Command(BaseCommand):
    help = 'Subscriber MQTT avec gestion des incidents, Gmail et Telegram'

    def handle(self, *args, **options):
        client = mqtt.Client(client_id="django-dht-subscriber")
        client.on_connect = on_connect
        client.on_message = on_message

        print(f"Connexion à {settings.MQTT_HOST}:{settings.MQTT_PORT}...")
        client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)

        # Boucle infinie pour écouter les messages MQTT
        client.loop_forever()
