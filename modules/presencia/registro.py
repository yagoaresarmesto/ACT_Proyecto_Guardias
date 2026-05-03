from modules.db.db_manager import (
    registrar_presencia,
    obtener_presentes,
    obtener_presencia,
    existe_presencia,
    borrar_presencia
)

def registrar(id_profesor, fecha, hora):
    registrar_presencia(id_profesor, fecha, hora)

def obtener_presentes_en_hora(fecha, hora):
    return obtener_presentes(fecha, hora)


def obtener_presencia_dia(fecha):
    return obtener_presencia(fecha)

def registrar_evento(profesor_id, fecha, hora):
    """
    Simula el comportamiento de un sistema real (RFID, huella, etc.)

    - Si el profesor NO está registrado → ENTRA
    - Si YA está registrado → SALE
    """

    profesor_id = int(profesor_id)
    hora = int(hora)

    if existe_presencia(profesor_id, fecha, hora):
        print(f"→ SALIDA | Profesor {profesor_id} | Hora {hora}")
        borrar_presencia(profesor_id, fecha, hora)
    else:
        print(f"→ ENTRADA | Profesor {profesor_id} | Hora {hora}")
        registrar(profesor_id, fecha, hora)