# DataScope

DataScope es una plataforma web para analizar conjuntos de datos de forma rápida e intuitiva.

## Objetivos

- Analizar archivos CSV
- Detectar valores nulos
- Obtener estadísticas descriptivas
- Visualizar los datos
- Guardar el historial de análisis

## Tecnologías

- Python
- FastAPI
- React
- TypeScript
- PostgreSQL

## Estado del proyecto

### V0.1 - Leer y analizar CSV básico

Funcionalidades implementadas:

- Lectura de archivos CSV.
- Comprobar la existencia del archivo.
- Comprobar la extensión.
- Número de filas.
- Número de columnas. 
- Valores nulos por columna.
- Filas duplicadas.

### V0.2 - API REST

Funcionalidades implementadas:

- API desarrollada con FastAPI.
- Endpoint 'GET /'
- Endpoint 'GET /health'
- Endpoint 'GET /analyze'
- Subida de archivos CSV.
- Análisis mediante 'analyze_csv()'
- Respuesta en formato JSON.
- Documentación automática con Swagger


## Hoja de ruta:
- [x] V0.1 Analizador básico de CSV
- [x] V0.2 API REST
- [] V0.3 Interfaz web
- [] V0.4 Base de datos
- [] V0.5 Sistema de usuarios
- [] V1.0 Primera versión estable

