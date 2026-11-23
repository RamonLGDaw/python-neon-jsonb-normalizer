from psycopg import sql
from psycopg.types.json import Jsonb
from normalizador import (
    DB_ID_COLUMN,
    DB_JSON_COLUMN,
    DB_TABLE,
    JSON_ARRAY_KEY,
    JSON_FIELD_KEY,
    normalizar_texto,
    obtener_conexion,
)

select_query = sql.SQL("""
    SELECT {id_col}, {json_col}
    FROM {table}
    WHERE {json_col} ? %s;
""").format(
    id_col=sql.Identifier(DB_ID_COLUMN),
    json_col=sql.Identifier(DB_JSON_COLUMN),
    table=sql.Identifier(DB_TABLE),
)

update_query = sql.SQL("""
    UPDATE {table}
    SET {json_col} = %s
    WHERE {id_col} = %s;
""").format(
    table=sql.Identifier(DB_TABLE),
    json_col=sql.Identifier(DB_JSON_COLUMN),
    id_col=sql.Identifier(DB_ID_COLUMN),
)

actualizadas = 0

with obtener_conexion() as conn:
    with conn.cursor() as cur:
        cur.execute(select_query, (JSON_ARRAY_KEY,))
        filas = cur.fetchall()

        for row_id, payload in filas:
            if not isinstance(payload, dict):
                continue

            items = payload.get(JSON_ARRAY_KEY)
            if not isinstance(items, list):
                continue

            hubo_cambio = False
            for item in items:
                if isinstance(item, dict) and isinstance(item.get(JSON_FIELD_KEY), str):
                    original = item[JSON_FIELD_KEY]
                    limpio = normalizar_texto(original)
                    if limpio != original:
                        item[JSON_FIELD_KEY] = limpio
                        hubo_cambio = True

            if hubo_cambio:
                cur.execute(update_query, (Jsonb(payload), row_id))
                actualizadas += 1

    conn.commit()

print(f"Listo. Filas actualizadas: {actualizadas}")