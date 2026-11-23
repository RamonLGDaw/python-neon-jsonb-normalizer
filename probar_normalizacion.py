from psycopg import sql
from normalizador import (
    DB_ID_COLUMN,
    DB_JSON_COLUMN,
    DB_TABLE,
    JSON_ARRAY_KEY,
    JSON_FIELD_KEY,
    normalizar_texto,
    obtener_conexion,
)

query = sql.SQL("""
    SELECT {id_col}, {json_col}
    FROM {table}
    WHERE {json_col} ? %s;
""").format(
    id_col=sql.Identifier(DB_ID_COLUMN),
    json_col=sql.Identifier(DB_JSON_COLUMN),
    table=sql.Identifier(DB_TABLE),
)

with obtener_conexion() as conn:
    with conn.cursor() as cur:
        cur.execute(query, (JSON_ARRAY_KEY,))
        filas = cur.fetchall()

filas_con_cambios = 0
total_cambios = 0

for row_id, payload in filas:
    if not isinstance(payload, dict):
        continue

    items = payload.get(JSON_ARRAY_KEY)
    if not isinstance(items, list):
        continue

    cambios_en_fila = []
    for item in items:
        if isinstance(item, dict) and isinstance(item.get(JSON_FIELD_KEY), str):
            original = item[JSON_FIELD_KEY]
            limpio = normalizar_texto(original)
            if limpio != original:
                cambios_en_fila.append((original, limpio))

    if cambios_en_fila:
        filas_con_cambios += 1
        total_cambios += len(cambios_en_fila)
        print(f"Fila ID {row_id}: {cambios_en_fila}")

print(f"\nResumen -> Filas afectadas: {filas_con_cambios} | Cambios detectados: {total_cambios}")