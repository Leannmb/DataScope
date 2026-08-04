# DataScope

DataScope es una plataforma web para analizar conjuntos de datos de forma rápida e intuitiva.

## Objetivos

- Analizar archivos CSV
- Detectar valores nulos
- Obtener estadísticas descriptivas
- Visualizar los datos
- Guardar el historial de análisis

## Tecnologías

### Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT
- Passlib (bcrypt)

### Frontend

- Vue 3
- TypeScript
- Vite
- CSS3

## Versiones 

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
- Endpoint GET /
- Endpoint GET /health
- Endpoint POST /analyze
- Subida de archivos CSV.
- Análisis mediante 'analyze_csv()'
- Respuesta en formato JSON.
- Documentación automática con Swagger

### V0.3 - Frontend 

Implementado:

- Frontend desarrollado con Vue.
- TypeScript.
- Selección de archivos CSV.
- Comunicación con la API mediante HTTP POST.
- Visualización de los resultados del análisis.
- Gestión de errores.
- Integración completa entre frontend y backend.

### V0.4 - Persistencia de datos

Funcionalidades implementadas:

- Integración con PostgreSQL.
- Modelado de datos mediante SQLAlchemy.
- Gestión de migraciones usando Alembic.
- Creación automática de la tabla 'analysis'.
- Persistencia de cada análisis realizado.
- Registro del nombre del archivo, número de filas, columnas y fecha de creación.

### V0.5 - Historial de análisis y mejora de la arquitectura

Funcionalidades implementadas:

- Consulta del historial de análisis.
- Visualización del historial desde el frontend.
- Navegación entre análisis e historial mediante pestañas.
- Refactorización del frontend mediante componentes reutilizables.
- Centralización de tipos TypeScript.
- Creación de un servicio dedicado para la comunicación con la API.
- Mejora de la interfaz de usuario.
- Diseño responsive.

### V0.6 - Sistema de autenticación

Funcionalidades implementadas:

- Sistema de registro de usuarios.
- Inicio de sesión mediante JWT
- Contraseñas almacenadas de forma segura mediante hash (bcrypt).
- Persistencia de la sesión mediante localStorage.
- Protección de endpoints mediante localStorage.
- Asociación de análisis a cada usuario.
- Consulta únicamente del historial del usuario autenticado. 
- Cierre de sesión. 
- Separación de la lógica de autenticación en servicios detallados



## Hoja de ruta:
- [x] V0.1 Analizador básico de CSV
- [x] V0.2 API REST
- [x] V0.3 Interfaz web
- [x] V0.4 Base de datos
- [x] V0.5 Historial de análisis y mejora de la arquitectura
- [x] V0.6 Sistema de autenticación de usuarios
- [] V0.7 Dashboard con estadísticas
- [] V0.8 Visualización de gráficos
- [] V0.9 Exportación de resultados
- [] V1.0 Primera versión estable

