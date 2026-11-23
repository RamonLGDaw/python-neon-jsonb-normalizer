import os
from dotenv import load_dotenv
import psycopg

load_dotenv()
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("No se encontró DATABASE_URL en el archivo .env")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user, version();")
        db_name, db_user, pg_version = cur.fetchone()
        print("¡Conexión exitosa!")
        print(f"Base de datos: {db_name} | Usuario: {db_user}")
        print(f"PostgreSQL: {pg_version}")