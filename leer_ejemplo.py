from psycopg import sql
from normalizador import (
    DB_ID_COLUMN,
    DB_JSON_COLUMN,
    DB_TABLE,
    JSON_ARRAY_KEY,
    JSON_FIELD_KEY,
    obtener_conexion,
)

query = sql.SQL("""
    SELECT {id_col}, {json_col}
    FROM {table}
    WHERE {json_col} ? %s
    LIMIT 1;
""").format(
    id_col=sql.Identifier(DB_ID_COLUMN),
    json_col=sql.Identifier(DB_JSON_COLUMN),
    table=sql.Identifier(DB_TABLE),
)

with obtener_conexion() as conn:
    with conn.cursor() as cur:
        cur.execute(query, (JSON_ARRAY_KEY,))
        row = cur.fetchone()

        if not row:
            print(f"No se encontró ninguna fila con '{JSON_ARRAY_KEY}'.")
        else:
            row_id, payload = row
            items = payload.get(JSON_ARRAY_KEY, []) if isinstance(payload, dict) else []
            print(f"Fila ID: {row_id} | Total {JSON_ARRAY_KEY}: {len(items)}")
            print(
                f"Primeros 3 {JSON_FIELD_KEY}:",
                [b.get(JSON_FIELD_KEY) for b in items[:3] if isinstance(b, dict)],
            )