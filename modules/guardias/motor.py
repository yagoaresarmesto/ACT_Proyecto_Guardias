from modules.db.db_manager import (
    obtener_horario_por_dia,
    obtener_presentes,
    crear_ausencia,
    crear_guardia,
    obtener_guardias,
    asignar_guardia,
    sumar_guardia
)

from modules.guardias.reglas import ordenar_por_guardias


def detectar_ausencias(dia_semana, fecha):
    horario = obtener_horario_por_dia(dia_semana)
    ausencias = []

    for h in horario:
        # Solo nos interesan clases
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
        crear_guardia(
            fecha,
            a["hora"],
            a["aula"],
            a["profesor"]
        )


def obtener_disponibles(dia_semana, fecha, hora):
    horario = obtener_horario_por_dia(dia_semana)

    presentes = obtener_presentes(fecha, hora)

    # Profesores ocupados (tienen clase en esa hora)
    ocupados = {
        h["id_profesor"]
        for h in horario
        if h["hora"] == hora and h["tipo"] == "clase"
    }

    disponibles = presentes - ocupados

    return disponibles


def asignar_guardias(dia_semana, fecha):
    guardias = obtener_guardias(fecha)

    for g in guardias:
        # Si ya está asignada, saltar
        if g["id_profesor_cubre"] is not None:
            continue

        hora = g["hora"]

        disponibles = obtener_disponibles(dia_semana, fecha, hora)

        if not disponibles:
            continue

        # Ordenar según reglas (guardias acumuladas, etc.)
        ranking = ordenar_por_guardias(disponibles)

        profesor_elegido = ranking[0]  # id profesor

        asignar_guardia(g["id_guardia"], profesor_elegido)
        sumar_guardia(profesor_elegido)


def generar_guardias(dia_semana, fecha):
    """
    Ejecuta todo el flujo:
    1. Detecta ausencias
    2. Crea guardias
    3. Asigna profesores
    """

    ausencias = detectar_ausencias(dia_semana, fecha)

    crear_guardias_desde_ausencias(ausencias, fecha)

    asignar_guardias(dia_semana, fecha)