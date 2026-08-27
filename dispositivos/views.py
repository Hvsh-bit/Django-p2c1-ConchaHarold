from django.shortcuts import render
from .services import cargar_dispositivos


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }

    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )


def catalogo(request):
    dispositivos = cargar_dispositivos()

    total_activos = sum(
        1
        for dispositivo in dispositivos
        if dispositivo["estado"] == "Activo"
    )

    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": total_activos,
    }

    return render(
        request,
        "dispositivos/catalogo.html",
        contexto,
    )