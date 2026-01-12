#views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Dht11, Incident
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
import csv
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView




class OperateurLoginView(LoginView):
    template_name = "login.html"

class OperateurLogoutView(LogoutView):
    next_page = "/login/"


@login_required
def dashboard(request):
    incident = Incident.objects.filter(is_open=True).order_by("-date_traitement").first()
    return render(request, "dashboard.html", {"incident": incident})

def latest_json(request):
    last = Dht11.objects.last()
    return JsonResponse({
        "temperature": last.temp if last else 0,
        "humidity": last.hum if last else 0,
        "timestamp": last.dt.isoformat() if last else None
    })

def incident_archive(request):
    incidents = Incident.objects.filter(is_open=False).order_by("-ended_at")
    return render(request, "incident_archive.html", {"incidents": incidents})

def incident_detail(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    return render(request, "incident_detail.html", {"incident": incident})

def valider_incident(request):
    Incident.objects.filter(is_open=True).update(is_open=False, ended_at=timezone.now())
    return HttpResponse("OK")

# --- EXPORT CSV FILTRÉ ---
# views.py
def export_csv_filtered(request):
    date_str = request.GET.get('date')
    period = request.GET.get('period', 'day')
    
    # Même logique de temps que dans l'API
    if date_str:
        # On crée une date naïve puis on la rend "aware" (consciente du fuseau horaire)
        naive_date = datetime.strptime(date_str, '%Y-%m-%d')
        base_date = make_aware(naive_date)
    else:
        base_date = timezone.now()

    if period == 'day':
        start_date = base_date.replace(hour=0, minute=0, second=0)
        end_date = base_date.replace(hour=23, minute=59, second=59)
    elif period == 'week':
        start_date = base_date - timedelta(days=7)
        end_date = base_date.replace(hour=23, minute=59, second=59)
    else: # Month
        start_date = base_date - timedelta(days=30)
        end_date = base_date.replace(hour=23, minute=59, second=59)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="export_{period}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date et Heure', 'Température', 'Humidité'])
    
    # Filtrage réel pour le CSV
    records = Dht11.objects.filter(dt__range=(start_date, end_date)).order_by('dt')
    
    for r in records:
        writer.writerow([r.dt.strftime("%d/%m/%Y %H:%M"), r.temp, r.hum])
        
    return response

def download_dht_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historique_dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date/Heure', 'Température', 'Humidité'])
    for d in Dht11.objects.all().order_by('-dt'):
        writer.writerow([d.dt.strftime("%Y-%m-%d %H:%M:%S"), d.temp, d.hum])
    return response

def download_incidents_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="incidents.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Début', 'Fin', 'Max Temp'])
    for i in Incident.objects.all(): writer.writerow([i.id, i.date_traitement, i.ended_at, i.max_temp])
    return response

def simulation_data(request):
    Dht11.objects.create(temp=random.uniform(0, 10), hum=random.uniform(40, 60))
    return HttpResponse("Donnée simulée ajoutée.")

def graph_temp(request): return render(request, 'graph_temp.html', {'timestamp': timezone.now().timestamp()})
def graph_hum(request):     return render(request, 'graph_hum.html', {'timestamp': timezone.now().timestamp()})



def latest_data(request):
    last = Dht11.objects.last()
    return JsonResponse({
        "temperature": last.temp if last else 0,
        "humidity": last.hum if last else 0
    })


