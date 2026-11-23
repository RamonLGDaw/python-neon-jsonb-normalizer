# Normalizar campos JSONB en Neon (PostgreSQL)

Pequeño proceso ETL en Python para limpiar datos históricos en Neon (PostgreSQL) y normalizar a mayúsculas y sin acentos un campo de texto (por defecto `parametro`) dentro de un array en una columna `JSONB` (por defecto `biomarcadores` en `datos_json` de la tabla `analiticas`).

Mantiene el orden original del array y el resto del documento `JSONB` intactos, actualizando únicamente las filas que presentan cambios.

## Estructura del proyecto

- `normalizador.py`: carga variables de entorno, gestiona la conexión a la base de datos y contiene la función de normalización sin acentos y en mayúsculas.
- `test_conexion.py`: verifica la conectividad y los datos básicos de conexión contra la base de datos configurada[cite: 1].
- `leer_ejemplo.py`: muestra una fila de ejemplo que contenga el array configurado para inspeccionar su estructura[cite: 1].
- `probar_normalizacion.py`: simula la normalización en memoria sin modificar la base de datos e informa de filas y cambios detectados[cite: 1].
- `aplicar_normalizacion.py`: aplica el `UPDATE` únicamente sobre las filas que tienen cambios reales[cite: 1].
- `requirements.txt`: dependencias del proyecto[cite: 1].
- `.gitignore`: excluye `.env`, `venv` y `.venv` del control de versiones[cite: 1].

## Requisitos y configuración

1. Crea y activa un entorno virtual e instala las dependencias[cite: 1]:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt


2. Crea un archivo .env a partir de .env.example
    ```bash
    DATABASE_URL=postgresql://usuario:contraseña@ep-ejemplo.region.aws.neon.tech/neondb?sslmode=require
    DB_TABLE=analiticas
    DB_ID_COLUMN=id
    DB_JSON_COLUMN=datos_json
    JSON_ARRAY_KEY=biomarcadores
    JSON_FIELD_KEY=parametro


## Flujo recomendado

1. Comprueba la conexión:
    ```bash
    python test_conexion.py

2. Inspecciona un registro de ejemplo:
    ```bash
    python leer_ejemplo.py

3. Simula los cambios en memoria sin escribir en la base de datos:
    ```bash
    python probar_normalizacion.py

4. Aplica la actualización sobre las filas con cambios:
    ```bash
    python aplicar_normalizacion.py

5. Vuelve a ejecutar python probar_normalizacion.py para confirmar que no quedan cambios pendientes.
    

