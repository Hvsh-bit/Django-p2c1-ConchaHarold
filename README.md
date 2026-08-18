# EcoEnergy

EcoEnergy es un proyecto estudiantil de backend desarrollado con Python y Django. Su objetivo es servir como base para una aplicación orientada al registro y la consulta de información sobre consumo energético, además de apoyar el seguimiento de prácticas de eficiencia energética.

El proyecto se encuentra en una etapa inicial, por lo que su alcance podrá ajustarse a medida que se definan los requisitos académicos y funcionales.

## Requisitos previos

Antes de comenzar, es necesario contar con:

- Git.
- Python 3.14.7, versión utilizada actualmente por el proyecto.
- `pip` y el módulo `venv` de Python.

Las dependencias de Python y sus versiones se encuentran definidas en `requirements.txt`.

## Clonación del repositorio

```bash
git clone https://github.com/Hvsh-bit/Django-p2c1-ConchaHarold.git
cd Django-p2c1-ConchaHarold
```

## Creación y activación del entorno virtual

Crear el entorno virtual en la raíz del proyecto:

```bash
python3 -m venv .venv
```

Activarlo en macOS o Linux:

```bash
source .venv/bin/activate
```

Para salir del entorno virtual:

```bash
deactivate
```

## Instalación de dependencias

Con el entorno virtual activado, instalar las dependencias declaradas en `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Comandos de verificación

Comprobar la versión de Python activa:

```bash
python --version
```

Comprobar la versión de Django instalada:

```bash
python -m django --version
```

Verificar que las dependencias instaladas sean compatibles:

```bash
python -m pip check
```

Ejecutar la revisión interna del proyecto Django:

```bash
python manage.py check
```

## Estado actual

Actualmente, EcoEnergy cuenta con:

- La estructura inicial de un proyecto Django.
- El módulo principal de configuración `config`.
- SQLite como base de datos de desarrollo.
- La ruta de administración proporcionada por Django.
- Las dependencias registradas en `requirements.txt`.
- La verificación de Django completada sin problemas detectados.

Todavía no se han creado aplicaciones de dominio ni funcionalidades propias de EcoEnergy.

## Próximos pasos

- Definir los requisitos funcionales del proyecto.
- Diseñar el modelo de datos para el registro del consumo energético.
- Crear la primera aplicación de dominio en Django.
- Implementar las interfaces necesarias para registrar y consultar información.
- Añadir pruebas automatizadas.
- Separar la configuración de desarrollo de una futura configuración de producción.
