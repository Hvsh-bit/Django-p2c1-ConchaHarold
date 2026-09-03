# EcoEnergy

EcoEnergy es una aplicación académica desarrollada con Django para consultar
zonas de consumo energético y los dispositivos instalados en ellas. Los datos
se almacenan en archivos JSON, las relaciones se resuelven con estructuras
Python y la presentación utiliza Templates de Django con Bootstrap 5.

## Alcance de la Fase 1

- Listado de zonas con límite energético y cantidad de dispositivos.
- Detalle de cada zona con dispositivos, categorías y consumo total.
- Estado `ALERTA` cuando el consumo supera el límite permitido.
- Estado `NORMAL` cuando el consumo es menor o igual al límite.
- Manejo de zonas sin dispositivos y zonas inexistentes.
- Lectura dinámica de JSON sin Models, ORM, CRUD ni formularios.

## Requisitos

- Python 3.12 o superior.
- Django 6.1.
- django-bootstrap5 26.2.

Las versiones utilizadas están fijadas en `requirements.txt`:

```text
asgiref==3.12.1
Django==6.1
django-bootstrap5==26.2
sqlparse==0.6.0
```

El módulo `json` pertenece a la biblioteca estándar de Python y no se instala
como dependencia externa.

## Fuente de datos

La carpeta `data/` contiene las tres colecciones solicitadas:

| Archivo | Campos | Cantidad actual |
| --- | --- | --- |
| `zonas.json` | `id`, `nombre`, `limite_kwh` | 3 zonas |
| `categorias.json` | `id`, `nombre`, `descripcion` | 3 categorías |
| `dispositivos.json` | `id`, `nombre`, `consumo_kwh`, `zona_id`, `categoria_id` | 8 dispositivos |

`zona_id` relaciona cada dispositivo con `zonas.id` y `categoria_id` lo
relaciona con `categorias.id`. Los archivos se cargan en cada solicitud, por lo
que los registros válidos agregados posteriormente se incorporan sin cambiar
la lógica de las Views.

## Flujo de la aplicación

```text
URL
 ↓
dispositivos/urls.py
 ↓
dispositivos/views.py
 ↓
dispositivos/services.py
 ↓
data/*.json
 ↓
contexto Python
 ↓
Template Django + Bootstrap 5
```

El servicio `cargar_json(nombre_archivo)` lee cualquier colección desde
`data/` y verifica que su raíz sea una lista. `buscar_por_id` permite resolver
las relaciones entre los diccionarios cargados.

## Estructura relevante

```text
Django-p2c1-ConchaHarold/
├── data/
│   ├── categorias.json
│   ├── dispositivos.json
│   └── zonas.json
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
│       ├── detalle_zona.html
│       ├── inicio.html
│       └── lista_zonas.html
├── ANALISIS.md
├── IA.md
├── manage.py
├── README.md
└── requirements.txt
```

## Instalación

Clona el repositorio y entra en su directorio:

```bash
git clone https://github.com/Hvsh-bit/Django-p2c1-ConchaHarold.git
cd Django-p2c1-ConchaHarold
```

Crea y activa un entorno virtual en macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell, crea y activa el entorno con:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala y comprueba las dependencias:

```bash
python -m pip install -r requirements.txt
python -m pip check
python manage.py migrate
```

La migración crea `db.sqlite3` en cada equipo. Este archivo y `.venv` son
locales y están excluidos por `.gitignore`, por lo que no se transfieren con
Git y deben volver a generarse después de clonar el repositorio.

## Ejecución

Desde la raíz del proyecto:

```bash
python manage.py check
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador.

## Reutilización en otro equipo

Antes de cambiar de equipo, revisa el estado. Si existen cambios pendientes,
agrégalos y crea un commit antes de enviarlos al repositorio remoto:

```bash
git status
git add .
git commit -m "Guarda avances del proyecto"
git push origin main
```

Si `git status` indica que no hay cambios pendientes, solo necesitas ejecutar
`git push origin main`.

En el equipo nuevo, sigue la sección de instalación desde `git clone`. No
copies `.venv` ni `db.sqlite3`: crea un entorno virtual nuevo, instala
`requirements.txt` y ejecuta las migraciones.

## Rutas funcionales

| URL | Nombre de URL | Función |
| --- | --- | --- |
| `/` | `dispositivos:inicio` | Página inicial. |
| `/zonas/` | `dispositivos:lista_zonas` | Lista las zonas y la cantidad de dispositivos de cada una. |
| `/zonas/<id>/` | `dispositivos:detalle_zona` | Muestra dispositivos, categorías, consumo total y estado de la zona. |

Por ejemplo, `http://127.0.0.1:8000/zonas/1/` abre el detalle de la zona con
identificador 1. Un identificador inexistente devuelve HTTP 404.

## Reglas de estado

```python
estado = "ALERTA" if total_consumo > limite_kwh else "NORMAL"
```

La comparación es estricta para `ALERTA`. Cuando el consumo total es igual al
límite, el resultado continúa siendo `NORMAL`.

## Pruebas y verificación

Ejecuta todas las comprobaciones desde la raíz:

```bash
python -m json.tool data/zonas.json
python -m json.tool data/categorias.json
python -m json.tool data/dispositivos.json
python -m pip check
python manage.py check
python manage.py test -v 2
```

La suite comprueba:

- El mínimo y el esquema exacto de las tres colecciones.
- La validez de `zona_id` y `categoria_id`.
- El rechazo de una raíz JSON que no sea una lista.
- El template y los conteos del listado de zonas.
- Las categorías, el consumo total y los estados del detalle.
- El comportamiento de una zona sin dispositivos.
- La respuesta 404 para una zona inexistente.

## Interfaz

Los Templates heredan de `templates/base.html` y utilizan Bootstrap 5 mediante
`django-bootstrap5`. Las tablas se encuentran dentro de contenedores
responsive, la navegación se adapta a pantallas pequeñas y los estados se
comunican con texto además de color.

## Documentación adicional

- `ANALISIS.md` describe las relaciones, multiplicidades, claves, reglas y la
  matriz de trazabilidad entre criterios y pruebas.
- `IA.md` registra la herramienta de IA utilizada, los prompts, las partes
  incorporadas, las decisiones del estudiante y la verificación realizada.

## Límites de esta fase

- La aplicación es de solo lectura.
- No utiliza base de datos para las colecciones de EcoEnergy.
- No incluye Models, migraciones de dominio, ORM, CRUD, autenticación ni
  permisos.
- La validación del loader comprueba la lista raíz; las pruebas verifican el
  esquema y las relaciones de los datos entregados.
