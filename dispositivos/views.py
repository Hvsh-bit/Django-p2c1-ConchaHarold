from collections import Counter

from django.http import Http404
from django.shortcuts import render

from .services import buscar_por_id, cargar_json


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


def lista_zonas(request):
    zonas = cargar_json("zonas.json")
    dispositivos = cargar_json("dispositivos.json")

    cantidades_por_zona = Counter(
        dispositivo["zona_id"]
        for dispositivo in dispositivos
    )

    zonas_con_resumen = [
        {
            **zona,
            "cantidad_dispositivos": cantidades_por_zona.get(
                zona["id"],
                0,
            ),
        }
        for zona in zonas
    ]

    return render(
        request,
        "dispositivos/lista_zonas.html",
        {"zonas": zonas_con_resumen},
    )


def detalle_zona(request, zona_id):
    zonas = cargar_json("zonas.json")
    zona = buscar_por_id(zonas, zona_id)

    if zona is None:
        raise Http404("Zona no encontrada")

    dispositivos = cargar_json("dispositivos.json")
    categorias = cargar_json("categorias.json")

    dispositivos_zona = []

    for dispositivo in dispositivos:
        if dispositivo["zona_id"] != zona_id:
            continue

        categoria = buscar_por_id(
            categorias,
            dispositivo["categoria_id"],
        )

        dispositivos_zona.append(
            {
                **dispositivo,
                "categoria_nombre": (
                    categoria["nombre"]
                    if categoria
                    else "Sin categoría"
                ),
            }
        )

    total_consumo = sum(
        dispositivo["consumo_kwh"]
        for dispositivo in dispositivos_zona
    )
    estado = (
        "ALERTA"
        if total_consumo > zona["limite_kwh"]
        else "NORMAL"
    )

    contexto = {
        "zona": zona,
        "dispositivos": dispositivos_zona,
        "total_consumo": total_consumo,
        "cantidad": len(dispositivos_zona),
        "estado": estado,
    }

    return render(
        request,
        "dispositivos/detalle_zona.html",
        contexto,
    )
