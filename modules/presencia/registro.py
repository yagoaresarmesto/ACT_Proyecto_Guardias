from modules.db.db_manager import (
    registrar_evento as guardar_evento,
    obtener_eventos,
    obtener_presentes,
    obtener_profesor_por_id,
    actualizar_rfid_uid_profesor,
)

from modules.presencia.facial import (
    capturar_referencia_profesor,
    capturar_verificacion_profesor,
)


def registrar_evento(profesor_id, fecha, hora):
    profesor_id = int(profesor_id)
    hora = int(hora)

    profesor = obtener_profesor_por_id(profesor_id)

    if profesor is None:
        print("Profesor no encontrado")
        return False

    # Si no tiene referencia facial, se crea
    if not profesor.rfid_uid:
        print(f"Profesor {profesor.nombre} sin referencia facial.")
        print("Capturando foto de referencia...")

        ruta_referencia = capturar_referencia_profesor(profesor_id)

        actualizar_rfid_uid_profesor(
            profesor_id,
            ruta_referencia
        )

        print("Referencia facial guardada.")
        print("Vuelve a registrar presencia para verificar.")

        return False

    # Si ya tiene referencia, capturamos foto de verificación
    print(f"Profesor {profesor.nombre} con referencia facial.")
    print("Capturando foto de verificación...")

    ruta_verificacion = capturar_verificacion_profesor(profesor_id)

    print("Foto de verificación guardada:", ruta_verificacion)

    # De momento aceptamos siempre.
    # Más adelante aquí irá la comparación facial real.
    verificado = True

    if not verificado:
        print("Verificación facial fallida.")
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