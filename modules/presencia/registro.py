from modules.db.db_manager import (
    registrar_presencia,
    obtener_presentes,
    obtener_presencia
)

def registrar(id_profesor, fecha, hora):
    registrar_presencia(id_profesor, fecha, hora)


def obtener_presentes_en_hora(fecha, hora):
    return obtener_presentes(fecha, hora)


def obtener_presencia_dia(fecha):
    return obtener_presencia(fecha)