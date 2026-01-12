#urls.py
from django.urls import path
from . import views, api
from .views import OperateurLoginView, OperateurLogoutView

urlpatterns = [
    # ---------------- Dashboard HTML ----------------
    path("", views.dashboard, name="dashboard"),

    # ---------------- API REST ----------------
    path("api/", api.Dlist, name="api_list"),             # GET historique
    path("api/post/", api.Dhtviews.as_view(), name="api_post"),  # POST ESP8266

    # ---------------- JSON pour JS / Dashboard ----------------
    path("latest/", views.latest_json, name="latest_json"),

    # ---------------- Validation incidents ----------------
    path("incident/valider", views.valider_incident, name="valider_incident"),

    # ---------------- Pages graphiques ----------------
    path("graph-temp/", views.graph_temp, name="graph-temp"),
    path("graph-hum/", views.graph_hum, name="graph-hum"),
    path("api/data/", api.data_filtered, name="api_data_filtered"),
    path('api/export_csv_filtered/', views.export_csv_filtered, name='export_csv_filtered'),


    # ---------------- Exports CSV ----------------
    path("download/dht", views.download_dht_csv, name="download_dht"),
    path("download/incidents", views.download_incidents_csv, name="download_incidents"),

    # ---------------- Simulation / Test manuel ----------------
    path("simulation/", views.simulation_data, name="simulation_data"),
    
    path("incident/status/", api.IncidentStatus.as_view(), name="incident_status"),
    path("incident/update/", api.IncidentUpdateOperator.as_view(), name="incident_update"),
    path("incident/archive/", views.incident_archive, name="incident_archive"),
    path("incident/<int:pk>/", views.incident_detail, name="incident_detail"),
    path("download-csv/", views.download_dht_csv, name="download_dht_csv"),


    path("login/", OperateurLoginView.as_view(), name="login"),
    path("logout/", OperateurLogoutView.as_view(), name="logout"),
    
    path("latest/", views.latest_data, name="latest"),

]
