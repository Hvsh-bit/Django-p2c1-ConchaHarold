# EcoEnergy

Un catálogo energético que separa los datos, el procesamiento y la presentación.

EcoEnergy es un proyecto estudiantil desarrollado con Python y Django. La implementación carga 4 dispositivos desde JSON, calcula un resumen con Python y prepara una vista Bootstrap para presentar 3 dispositivos activos.

## Recorrido de los datos

```text
data/dispositivos.json
          ↓
dispositivos.services.cargar_dispositivos()
          ↓
dispositivos.views.catalogo()
          ↓
contexto: dispositivos, total, total_activos
          ↓
templates/dispositivos/catalogo.html
```

La colección contiene cuatro registros con las mismas claves:

| Clave | Responsabilidad |
| --- | --- |
| `id` | Identificador del dispositivo. |
| `nombre` | Nombre presentado en el catálogo. |
| `estado` | Estado utilizado para el resumen y el badge. |
| `consumo_kwh` | Consumo mostrado en kWh. |

El loader abre el archivo con codificación UTF-8, transforma el JSON en estructuras Python y valida que el elemento raíz sea una lista. La view carga la colección una sola vez, calcula el total y cuenta los registros cuyo estado es `Activo`.

## Estado actual

Comprobaciones ejecutadas el 27 de agosto de 2026:

| Comprobación | Resultado |
| --- | --- |
| `python -m json.tool data/dispositivos.json` | JSON válido. |
| Cantidad de registros | 4 dispositivos. |
| Dispositivos activos | 3 dispositivos. |
| `python -m pip check` | No se encontraron dependencias incompatibles. |
| `python manage.py check` | Sin problemas de configuración detectados. |
| `python manage.py test` | 7 pruebas encontradas: 2 pasan y 5 quedan bloqueadas por el registro pendiente de `django_bootstrap5`. |

> [!IMPORTANT]
> `django-bootstrap5` está instalado y fijado en `requirements.txt`, pero el checkout actual todavía debe agregar `"django_bootstrap5"` a `INSTALLED_APPS` en `config/settings.py`. Sin ese registro, Django no puede cargar `{% load django_bootstrap5 %}` y las pruebas de las vistas terminan con `TemplateSyntaxError`.

## Requisitos comprobados

El entorno virtual local utiliza:

- Python 3.14.7.
- Django 6.1.
- django-bootstrap5 26.2.

Las versiones reproducibles están fijadas en `requirements.txt`:

```text
asgiref==3.12.1
Django==6.1
django-bootstrap5==26.2
sqlparse==0.6.0
```

`json` no aparece en `requirements.txt` porque forma parte de la biblioteca estándar de Python.

## Estructura relevante

```text
Django-p2c1-ConchaHarold/
├── data/
│   └── dispositivos.json
├── config/
│   ├── settings.py
│   └── urls.py
├── dispositivos/
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── dispositivos/
│       ├── catalogo.html
│       └── inicio.html
├── manage.py
└── requirements.txt
```

Cada archivo tiene una responsabilidad definida:

| Archivo | Responsabilidad |
| --- | --- |
| `data/dispositivos.json` | Mantiene la colección fuera del código Python. |
| `dispositivos/services.py` | Carga y valida la estructura JSON. |
| `dispositivos/views.py` | Calcula el resumen y construye el contexto. |
| `templates/dispositivos/catalogo.html` | Presenta tarjetas, tabla, badges y estado vacío. |
| `dispositivos/tests.py` | Comprueba el loader, el contexto, el template y el estado vacío. |

## Contexto de los templates

| Template | Variables disponibles |
| --- | --- |
| `templates/dispositivos/inicio.html` | `sistema`, `mensaje`, `asignatura` |
| `templates/dispositivos/catalogo.html` | `dispositivos`, `total`, `total_activos` |

Cada elemento de `dispositivos` contiene `id`, `nombre`, `estado` y `consumo_kwh`.

## Rutas registradas

| URL | Nombre | View | Template |
| --- | --- | --- | --- |
| `/` | `dispositivos:inicio` | `dispositivos.views.inicio` | `dispositivos/inicio.html` |
| `/dispositivos/` | `dispositivos:catalogo` | `dispositivos.views.catalogo` | `dispositivos/catalogo.html` |
| `/admin/` | Administración de Django | `admin.site.urls` | Templates del admin |

## Instalación

Clona el repositorio y entra en su directorio:

```bash
git clone https://github.com/Hvsh-bit/Django-p2c1-ConchaHarold.git
cd Django-p2c1-ConchaHarold
```

Crea y activa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

Registra la integración Bootstrap en `config/settings.py`:

```python
INSTALLED_APPS = [
    # Aplicaciones de Django
    "django_bootstrap5",
    "dispositivos",
]
```

La entrada anterior se agrega a la lista existente. No se deben eliminar las aplicaciones incluidas por Django.

## Ejecución

Comprueba la configuración e inicia el servidor:

```bash
python manage.py check
python manage.py runserver
```

La aplicación queda disponible en `http://127.0.0.1:8000/` y el catálogo en `http://127.0.0.1:8000/dispositivos/`.

## Verificación

Ejecuta las comprobaciones desde la raíz del proyecto:

```bash
python -m json.tool data/dispositivos.json
python -m pip check
python manage.py check
python manage.py test -v 2
```

Después de registrar `django_bootstrap5`, la suite debe ejecutar estas siete pruebas:

- La ruta del catálogo responde y usa el template esperado.
- El contexto contiene un total de 4 y un total activo de 3.
- El catálogo recibe cuatro dispositivos.
- La página presenta el resumen y los datos de consumo.
- Una colección vacía presenta un mensaje comprensible.
- El loader carga la colección JSON.
- El loader rechaza un elemento raíz que no sea una lista.

## Justificación de la dependencia externa

| Evidencia | Decisión |
| --- | --- |
| Necesidad | Presentar el catálogo con una interfaz legible y responsive. |
| Uso | `base.html` carga los recursos mediante las etiquetas de `django_bootstrap5`. |
| Comprobación | `pip check`, `manage.py check`, la suite y la revisión en el navegador permiten verificar la integración. |
| Reproducibilidad | `django-bootstrap5==26.2` está fijado en `requirements.txt`. |

## Decisiones de diseño

1. Los datos viven en JSON para que un cambio de registros no obligue a modificar la view.
2. Los cálculos se realizan en Python para que el template se concentre en la presentación.
3. La tabla usa un contenedor responsive, encabezados semánticos, badges con texto y un estado vacío verificable.

## Límites actuales

- JSON mejora la separación de responsabilidades, pero no reemplaza una base de datos.
- El loader comprueba que la raíz sea una lista, pero todavía no valida el tipo de cada campo individual.
- El catálogo es de solo lectura y no permite crear, editar ni eliminar dispositivos.
- No existen modelos de dominio ni persistencia de dispositivos en SQLite.
- La integración visual depende de recursos Bootstrap cargados por `django-bootstrap5`.
