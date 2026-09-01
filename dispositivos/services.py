import json

from django.conf import settings


def cargar_json(nombre_archivo):
    ruta = settings.BASE_DIR / "data" / nombre_archivo

    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, list):
        raise ValueError(f"{nombre_archivo} debe contener una lista")

    return datos


def buscar_por_id(coleccion, identificador):
    return next(
        (
            item
            for item in coleccion
            if item["id"] == identificador
        ),
        None,
    )