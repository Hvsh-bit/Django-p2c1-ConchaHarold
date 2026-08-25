# EcoEnergy

EcoEnergy es un proyecto estudiantil desarrollado con Python y Django. La implementación actual muestra una página de inicio y un catálogo de dispositivos mediante vistas, plantillas de Django y navegación por URLs con nombre.

Los datos del catálogo están definidos directamente en `dispositivos/views.py`; por ahora no existen modelos de dominio ni persistencia propia para esos dispositivos.

## Requisitos comprobados

El entorno virtual local del proyecto utiliza:

- Python 3.14.7.
- Django 6.1.

Las dependencias instalables están fijadas en `requirements.txt`:

- `asgiref==3.12.1`
- `Django==6.1`
- `sqlparse==0.6.0`

## Estructura relevante

```text
Django-p2c1-ConchaHarold/
├── manage.py
├── requirements.txt
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dispositivos/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── templates/
    ├── base.html
    └── dispositivos/
        ├── catalogo.html
        └── inicio.html
```

`config/settings.py` registra la aplicación `dispositivos` y configura el directorio `templates` para que Django encuentre las plantillas del proyecto.

## Plantillas y claves de contexto

| Plantilla | Relación | Claves utilizadas |
| --- | --- | --- |
| `templates/base.html` | Plantilla base con los bloques `title` y `content`; contiene enlaces a Inicio y Dispositivos. | No recibe claves propias. |
| `templates/dispositivos/inicio.html` | Extiende `base.html`. | `sistema`, `mensaje`, `asignatura` |
| `templates/dispositivos/catalogo.html` | Extiende `base.html` y recorre la colección de dispositivos. | `dispositivos`; cada elemento contiene `nombre` y `estado`. |

## Rutas funcionales

| URL | Nombre de ruta | Vista | Plantilla | Resultado comprobado |
| --- | --- | --- | --- | --- |
| `/` | `dispositivos:inicio` | `dispositivos.views.inicio` | `dispositivos/inicio.html` | HTTP 200 |
| `/dispositivos/` | `dispositivos:catalogo` | `dispositivos.views.catalogo` | `dispositivos/catalogo.html` | HTTP 200 |

Django también expone `/admin/`. Un usuario sin sesión es redirigido a `/admin/login/?next=/admin/`.

## Instalación y ejecución

Clonar el repositorio y entrar en su directorio:

```bash
git clone https://github.com/Hvsh-bit/Django-p2c1-ConchaHarold.git
cd Django-p2c1-ConchaHarold
```

Crear y activar un entorno virtual en macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias y comprobar la configuración:

```bash
python -m pip install -r requirements.txt
python manage.py check
```

Iniciar el servidor de desarrollo desde la raíz del proyecto:

```bash
python manage.py runserver
```

La aplicación queda disponible en `http://127.0.0.1:8000/`.

## Prueba de navegación

Con el servidor en ejecución:

1. Abrir `http://127.0.0.1:8000/`. Debe mostrarse el título **EcoEnergy**, el mensaje **Monitoreo energético responsable** y el curso **Programación Back End**.
2. Seleccionar **Dispositivos** en la navegación. La URL debe cambiar a `http://127.0.0.1:8000/dispositivos/` y debe mostrarse el catálogo con Medidor inteligente, Sensor de temperatura y Climatizador.
3. Seleccionar **Inicio** para regresar a `http://127.0.0.1:8000/`.

También se pueden comprobar las respuestas de ambas rutas sin iniciar el servidor:

```bash
python manage.py shell -c "from django.test import Client; c = Client(); print([(url, c.get(url, HTTP_HOST='localhost').status_code) for url in ('/', '/dispositivos/')])"
```

El resultado esperado con la implementación actual es:

```text
[('/', 200), ('/dispositivos/', 200)]
```

## Pruebas automatizadas actuales

`dispositivos/tests.py` no contiene casos de prueba. Por esa razón, `python manage.py test` encuentra 0 pruebas; la comprobación anterior valida únicamente que las dos rutas públicas se resuelven y responden correctamente.
