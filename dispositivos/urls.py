from django.urls import path
from . import views

app_name = "dispositivos"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("zonas/", views.lista_zonas, name="lista_zonas"),
    path(
        "zonas/<int:zona_id>/",
        views.detalle_zona,
        name="detalle_zona",
    ),
    path("resumen-zonas/", views.resumen_zonas, name="resumen_zonas"),
]

