import os
import unicodedata
from dotenv import load_dotenv
import psycopg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_TABLE = os.getenv("DB_TABLE", "analiticas")
DB_ID_COLUMN = os.getenv("DB_ID_COLUMN", "id")
DB_JSON_COLUMN = os.getenv("DB_JSON_COLUMN", "datos_json")
JSON_ARRAY_KEY = os.getenv("JSON_ARRAY_KEY", "biomarcadores")
JSON_FIELD_KEY = os.getenv("JSON_FIELD_KEY", "parametro")


def normalizar_texto(texto: str) -> str:
    """Descompone caracteres con tilde y quita marcas diacríticas (tildes, diéresis, etc.)."""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return sin_acentos.upper()


def obtener_conexion():
    if not DATABASE_URL:
        raise ValueError("No se encontró DATABASE_URL en el archivo .env")
    return psycopg.connect(DATABASE_URL)