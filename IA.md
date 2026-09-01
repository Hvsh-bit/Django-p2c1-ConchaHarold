# Registro de uso de inteligencia artificial

## Herramienta utilizada

- Herramienta: OpenAI Codex.
- Uso: apoyo durante la Fase 1 de EcoEnergy.
- Alcance: análisis de requisitos, revisión de código, pruebas, Templates
  Bootstrap 5 y documentación.

La IA se utilizó como apoyo y no como sustituto de la revisión del estudiante.
Cada cambio se contrastó con el enunciado y se ejecutaron comprobaciones locales
antes de conservarlo.

## Prompts y respuestas utilizadas

| Prompt o solicitud | Respuesta utilizada | Aplicación en el proyecto |
| --- | --- | --- |
| “¿Qué me recomiendas para continuar? ¿Leíste bien el contexto del PDF?” | Resumen del alcance obligatorio, los tres JSON, las rutas y los casos límite. | Se definió el orden de trabajo y se descartó el uso de Models, ORM y CRUD. |
| “Te entrego una recomendación de mejoras que me dio mi profesor.” | Comparación de la guía de clase con el enunciado de evaluación. | Se adoptó la separación URL, View, servicio y Template, además de URLs con nombre. |
| “Acabo de cambiar el `services.py`, ¿quedó bien?” | Revisión del loader genérico y propuesta de `buscar_por_id`. | Se consolidaron `cargar_json(nombre_archivo)` y `buscar_por_id(coleccion, identificador)`. |
| “Agrégala tú para que funcione.” | Propuesta de pruebas y relaciones entre las tres colecciones. | Se agregaron datos relacionados y pruebas de integridad referencial. |
| “Vamos, hay que continuar.” | Implementación guiada por pruebas del listado y detalle de zonas. | Se incorporaron rutas, cálculos, 404, estado vacío y Templates Bootstrap 5. |
| “Haz el siguiente paso y el siguiente también.” | Limpieza del catálogo heredado y preparación de la documentación obligatoria. | Se dejó el esquema exacto de dispositivos y se crearon `ANALISIS.md`, `IA.md` y un README actualizado. |

## Partes de la respuesta incorporadas

- Loader JSON genérico basado en `settings.BASE_DIR`.
- Búsqueda de registros por identificador mediante estructuras Python.
- Conteo de dispositivos por zona.
- Resolución de `zona_id` y `categoria_id` sin ORM.
- Cálculo de consumo total y estados `NORMAL` y `ALERTA`.
- Pruebas para rutas, contexto, relaciones, 404 y zona vacía.
- Estructura responsive con Bootstrap 5, tablas semánticas y estados expresados
  mediante texto y color.
- Organización de la documentación según los entregables del enunciado.

## Cambios y decisiones del estudiante

- Se creó y configuró inicialmente el proyecto Django y su aplicación.
- Se modificó `services.py` durante el trabajo guiado y luego se revisó su
  comportamiento con pruebas.
- Se entregaron los documentos del profesor como fuente de requisitos.
- Se revisaron y autorizaron los bloques de cambios antes de aplicarlos.
- Se decidió retirar el catálogo preliminar porque utilizaba una clave `estado`
  que no pertenece al esquema obligatorio de los dispositivos.
- Se mantuvo Bootstrap 5 como dependencia visual del proyecto.

## Verificación realizada

Durante el desarrollo se aplicó el ciclo prueba fallida, implementación mínima y
prueba aprobada. Las comprobaciones utilizadas fueron:

```bash
python -m json.tool data/zonas.json
python -m json.tool data/categorias.json
python -m json.tool data/dispositivos.json
python -m pip check
python manage.py check
python manage.py test -v 2
git diff --check
```

También se revisaron `/zonas/` y `/zonas/1/` en el navegador con tamaños de
1280 × 800 y 375 × 812 píxeles. Se comprobó la navegación responsive, el
contenido de las tablas y la ausencia de desbordamiento general.

## Comprensión y responsabilidad

El estudiante debe poder explicar el flujo MVT, las relaciones entre archivos,
los cálculos y las pruebas incluidas. El uso de IA corresponde únicamente a la
Fase 1 asistida y no autoriza su uso durante una instancia de evaluación que lo
prohíba.
