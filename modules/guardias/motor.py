from modules.db.db_manager import (
    obtener_horario_por_dia,
    obtener_presentes,
    crear_ausencia,
    crear_guardia,
    existe_guardia
)

from modules.guardias.reglas import ordenar_por_guardias


def detectar_ausencias(dia_semana, fecha):
    horario = obtener_horario_por_dia(dia_semana)
    ausencias = []

    for h in horario:
        if h["tipo"] != "clase":
            continue

        hora = h["hora"]
        profesor = h["id_profesor"]
        aula = h["aula"]

        presentes = obtener_presentes(fecha, hora)

        if profesor not in presentes:
            ausencias.append({
                "profesor": profesor,
                "hora": hora,
                "aula": aula
            })

            crear_ausencia(profesor, fecha, hora)

    return ausencias


def crear_guardias_desde_ausencias(ausencias, fecha):
    for a in ausencias:
        if not existe_guardia(fecha, a["hora"], a["aula"]):
            crear_guardia(
                fecha,
                a["hora"],
                a["aula"],
                a["profesor"]
            )


def obtener_disponibles(dia_semana, fecha, hora):
    horario = obtener_horario_por_dia(dia_semana)
    presentes = obtener_presentes(fecha, hora)

    ocupados = {
        h["id_profesor"]
        for h in horario
        if h["hora"] == hora and h["tipo"] == "clase"
    }

    disponibles = presentes - ocupados

    return disponibles


def obtener_ranking_guardia(dia_semana, fecha, hora):
    disponibles = obtener_disponibles(dia_semana, fecha, hora)

    if not disponibles:
        return []

    return ordenar_por_guardias(disponibles)


def generar_guardias(dia_semana, fecha):
    ausencias = detectar_ausencias(dia_semana, fecha)
    crear_guardias_desde_ausencias(ausencias, fecha)