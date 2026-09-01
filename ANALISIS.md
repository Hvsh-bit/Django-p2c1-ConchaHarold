# Análisis de EcoEnergy

## Objetivo de la solución

EcoEnergy permite consultar zonas de consumo energético y revisar los
dispositivos instalados en cada una. La Fase 1 utiliza archivos JSON como
fuente de datos, estructuras Python para resolver relaciones y Templates de
Django con Bootstrap 5 para presentar los resultados.

La solución no utiliza Models, ORM, formularios, autenticación ni operaciones
CRUD. Los datos se cargan nuevamente en cada solicitud, por lo que agregar
registros válidos a los archivos JSON no exige modificar el código.

## Colecciones y claves

### Zonas

Archivo: `data/zonas.json`

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | entero | Clave primaria lógica de la zona. |
| `nombre` | texto | Nombre visible de la zona. |
| `limite_kwh` | número | Consumo máximo permitido en kWh. |

### Categorías

Archivo: `data/categorias.json`

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | entero | Clave primaria lógica de la categoría. |
| `nombre` | texto | Nombre visible de la categoría. |
| `descripcion` | texto | Explicación del tipo de dispositivo. |

### Dispositivos

Archivo: `data/dispositivos.json`

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | entero | Clave primaria lógica del dispositivo. |
| `nombre` | texto | Nombre visible del dispositivo. |
| `consumo_kwh` | número | Consumo energético del dispositivo. |
| `zona_id` | entero | Clave foránea lógica hacia `zonas.id`. |
| `categoria_id` | entero | Clave foránea lógica hacia `categorias.id`. |

## Relaciones y multiplicidades

```text
Zona (1) ──────── (0..N) Dispositivo (0..N) ──────── (1) Categoría
  id                       zona_id                       id
                           categoria_id
```

| Relación | Multiplicidad | Clave de conexión | Regla |
| --- | --- | --- | --- |
| Zona - Dispositivo | Una zona puede tener cero o muchos dispositivos. Cada dispositivo pertenece a una zona. | `dispositivos.zona_id = zonas.id` | Todo `zona_id` debe existir en `zonas.json`. |
| Categoría - Dispositivo | Una categoría puede clasificar cero o muchos dispositivos. Cada dispositivo pertenece a una categoría. | `dispositivos.categoria_id = categorias.id` | Todo `categoria_id` debe existir en `categorias.json`. |

No existe una relación directa entre zona y categoría. La relación se obtiene a
través de los dispositivos instalados en la zona.

## Flujo MVT

```text
URL solicitada
      ↓
dispositivos/urls.py
      ↓
dispositivos/views.py
      ↓
dispositivos/services.py
      ↓
data/*.json → listas y diccionarios Python
      ↓
contexto calculado por la View
      ↓
Template heredado de base.html + Bootstrap 5
```

`cargar_json(nombre_archivo)` localiza la colección dentro de `data/`, la
decodifica en UTF-8 y comprueba que el elemento raíz sea una lista.
`buscar_por_id(coleccion, identificador)` resuelve una relación por su clave y
devuelve `None` cuando no encuentra el registro.

## Reglas de negocio

Para una zona seleccionada:

1. Se filtran los dispositivos cuyo `zona_id` coincide con `zona.id`.
2. Cada `categoria_id` se resuelve contra `categorias.json`.
3. `cantidad` corresponde al número de dispositivos filtrados.
4. `total_consumo` corresponde a la suma de sus valores `consumo_kwh`.
5. El estado es `ALERTA` cuando `total_consumo > limite_kwh`.
6. El estado es `NORMAL` cuando `total_consumo <= limite_kwh`.

Una zona sin dispositivos produce cantidad y consumo iguales a cero, por lo que
su estado es `NORMAL`. Un identificador de zona inexistente produce una
respuesta HTTP 404.

## Matriz de trazabilidad

| Criterio de aceptación | Archivo o componente | Prueba |
| --- | --- | --- |
| Existen al menos 3 zonas, 3 categorías y 8 dispositivos. | `data/zonas.json`, `data/categorias.json`, `data/dispositivos.json` | `CargarJsonTests.test_carga_minimo_tres_zonas`, `test_carga_minimo_tres_categorias` y `test_carga_coleccion_dispositivos_requerida`. |
| Los dispositivos usan exactamente las claves solicitadas. | `data/dispositivos.json` | `CargarJsonTests.test_carga_coleccion_dispositivos_requerida`. |
| Las claves foráneas lógicas apuntan a registros existentes. | Los tres archivos JSON | `CargarJsonTests.test_dispositivos_referencian_datos_existentes`. |
| El listado `/zonas/` muestra nombre, límite, cantidad y acceso al detalle. | `lista_zonas`, `dispositivos/urls.py`, `lista_zonas.html` | `ZonasViewTests.test_listado_zonas_responde_y_utiliza_su_template` y `test_listado_zonas_calcula_cantidad_dispositivos`. |
| El detalle resuelve dispositivos y categorías. | `detalle_zona`, `buscar_por_id`, `detalle_zona.html` | `ZonasViewTests.test_detalle_zona_prepara_metricas_y_categorias`. |
| `ALERTA` se aplica cuando el total supera el límite. | `detalle_zona` y `detalle_zona.html` | `ZonasViewTests.test_detalle_zona_prepara_metricas_y_categorias`. |
| `NORMAL` se aplica cuando el total no supera el límite. | `detalle_zona` y `detalle_zona.html` | `ZonasViewTests.test_detalle_zona_informa_estado_normal`. |
| Una zona sin dispositivos se presenta sin errores. | `detalle_zona` y estado vacío del template | `ZonasViewTests.test_detalle_zona_maneja_una_zona_sin_dispositivos`. |
| Una zona inexistente responde con 404. | `detalle_zona` | `ZonasViewTests.test_detalle_zona_inexistente_responde_404`. |
| El JSON debe contener una lista en la raíz. | `cargar_json` | `CargarJsonTests.test_rechaza_un_elemento_raiz_que_no_sea_lista`. |
| La interfaz hereda de `base.html`, usa Bootstrap 5 y mantiene tablas accesibles en pantallas pequeñas. | `base.html`, `lista_zonas.html`, `detalle_zona.html` | Revisión en navegador a 1280 px y 375 px, sin desbordamiento general. |

## Casos de prueba manual

| Caso | Resultado esperado |
| --- | --- |
| Abrir `/zonas/`. | Se muestran todas las zonas y la cantidad calculada de dispositivos. |
| Abrir `/zonas/1/`. | Se muestra un consumo total de 58,6 kWh y estado `ALERTA`. |
| Abrir `/zonas/2/`. | Se muestra un consumo total de 32,3 kWh y estado `NORMAL`. |
| Abrir `/zonas/999/`. | El servidor responde con HTTP 404. |
| Agregar un dispositivo válido a una zona. | El listado, la cantidad y el total cambian sin editar la View. |
| Dejar una zona sin dispositivos. | El detalle muestra el mensaje de estado vacío, cero dispositivos y estado `NORMAL`. |
