from django.urls import path
from . import views
from . import api

urlpatterns = [

    # API REST LIST
    path("api/", api.Dlist, name='json'),

    # POST depuis ESP8266
    path("api/post", api.Dhtviews.as_view(), name='api_post'),

    # PAGE DASHBOARD
    path("", views.dashboard, name="dashboard"),

    # JSON dernière mesure
    path("latest/", views.latest_json, name="latest_json"),

    # Graphiques
    path("graph-temp/", views.graph_temp, name="graph-temp"),
    path("graph-hum/", views.graph_hum, name="graph-hum"),
]
