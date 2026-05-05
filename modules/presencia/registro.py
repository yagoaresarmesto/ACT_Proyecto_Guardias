from modules.db.db_manager import (
    registrar_evento as guardar_evento,
    obtener_eventos,
    obtener_presentes
)


def registrar_evento(profesor_id, fecha, hora):

    profesor_id = int(profesor_id)
    hora = int(hora)

    eventos = obtener_eventos(fecha)

    eventos_profesor = sorted(
        [e for e in eventos if e["id_profesor"] == profesor_id],
        key=lambda x: x["hora"]
    )

    if any(e["hora"] == hora for e in eventos_profesor):
        print("⚠️ Ya existe evento en esta hora → ignorado")
        return

    if not eventos_profesor:
        tipo = "entrada"
    else:
        ultimo = eventos_profesor[-1]["tipo"]

        if ultimo == "entrada":
            tipo = "salida"
        else:
            tipo = "entrada"

    print(f"→ {tipo.upper()} | Profesor {profesor_id} | Hora {hora}")

    guardar_evento(profesor_id, fecha, hora, tipo)


def obtener_presencia_dia(fecha):
    return obtener_eventos(fecha)


def obtener_presentes_actuales(fecha):
    return obtener_presentes(fecha)


def obtener_presentes_en_hora(fecha, hora):
    return obtener_presentes(fecha)(fecha)