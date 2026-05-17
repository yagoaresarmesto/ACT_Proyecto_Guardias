from modules.db.db_manager import (
    registrar_evento as guardar_evento,
    obtener_eventos,
    obtener_presentes,
    obtener_profesor_por_id,
    actualizar_rfid_uid_profesor,
)

from modules.presencia.facial import (
    registrar_referencias_profesor,
    verificar_profesor_en_vivo,
)


def registrar_evento(profesor_id, fecha, hora):
    profesor_id = int(profesor_id)
    hora = int(hora)

    profesor = obtener_profesor_por_id(profesor_id)

    if profesor is None:
        print("Profesor no encontrado")
        return False

    # Si no tiene referencias faciales, se crean varias
    if not profesor.rfid_uid:
        print(f"Profesor {profesor.nombre} sin referencias faciales.")
        print("Iniciando registro facial...")

        ruta_encodings = registrar_referencias_profesor(profesor_id)

        if not ruta_encodings:
            print("No se pudo crear referencia facial.")
            return False

        actualizar_rfid_uid_profesor(
            profesor_id,
            ruta_encodings
        )

        print("Referencias faciales guardadas.")
        print("Vuelve a registrar presencia para verificar.")

        return False

    # Si ya tiene referencias, verificamos en vivo
    print(f"Profesor {profesor.nombre} con referencias faciales.")
    print("Iniciando verificaci�n en vivo...")

    verificado = verificar_profesor_en_vivo(
        profesor.rfid_uid
    )

    if not verificado:
        print("Verificaci�n facial fallida.")
        return False

    eventos = obtener_eventos(fecha)

    eventos_profesor = sorted(
        [e for e in eventos if e["id_profesor"] == profesor_id],
        key=lambda x: x["hora"]
    )

    if any(e["hora"] == hora for e in eventos_profesor):
        print("Ya existe evento en esta hora. Ignorado.")
        return False

    if not eventos_profesor:
        tipo = "entrada"
    else:
        ultimo = eventos_profesor[-1]["tipo"]

        if ultimo == "entrada":
            tipo = "salida"
        else:
            tipo = "entrada"

    print(f"{tipo.upper()} | Profesor {profesor_id} | Hora {hora}")

    guardar_evento(profesor_id, fecha, hora, tipo)

    return True


def obtener_presencia_dia(fecha):
    return obtener_eventos(fecha)


def obtener_presentes_actuales(fecha):
    return obtener_presentes(fecha)


def obtener_presentes_en_hora(fecha, hora):
    return obtener_presentes(fecha)