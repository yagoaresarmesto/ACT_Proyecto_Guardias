from modules.db.db_manager import (
    obtener_horario_por_dia,
    obtener_presentes,
    crear_ausencia,
    crear_guardia,
    existe_guardia,
    obtener_profesores_asignados
)

from modules.guardias.reglas import ordenar_por_guardias
from modules.guardias.models import Guardia as GuardiaDominio


# DETECTAR AUSENCIAS
def detectar_ausencias(dia_semana, fecha):
    horario = obtener_horario_por_dia(dia_semana)
    presentes = obtener_presentes(fecha)
    ausencias = []

    for h in horario:
        if h["tipo"] != "clase":
            continue

        hora = h["hora"]
        profesor = h["id_profesor"]
        aula = h["aula"]

        if profesor not in presentes:
            ausencia = GuardiaDominio(
                hora=hora,
                aula=aula,
                id_profesor_ausente=profesor
            )

            ausencias.append(ausencia)
            crear_ausencia(profesor, fecha, hora)

    return ausencias


# CREAR GUARDIAS
def crear_guardias_desde_ausencias(ausencias, fecha):
    for a in ausencias:
        if not existe_guardia(fecha, a.hora, a.aula):
            crear_guardia(
                fecha,
                a.hora,
                a.aula,
                a.id_profesor_ausente
            )


# DISPONIBLES
def obtener_disponibles(dia_semana, fecha, hora, hora_actual=None):
    horario = obtener_horario_por_dia(dia_semana)
    presentes = obtener_presentes(fecha)

    if hora_actual is not None and hora < hora_actual:
        return set()

    ocupados = {
        h["id_profesor"]
        for h in horario
        if h["hora"] == hora and h["tipo"] == "clase"
    }

    asignados = obtener_profesores_asignados(fecha, hora)

    disponibles = presentes - ocupados - asignados

    return disponibles


# RANKING
def obtener_ranking_guardia(dia_semana, fecha, hora, hora_actual=None):
    disponibles = obtener_disponibles(
        dia_semana,
        fecha,
        hora,
        hora_actual
    )

    if not disponibles:
        return []

    return ordenar_por_guardias(disponibles)


# GENERAR GUARDIAS
def generar_guardias(dia_semana, fecha):
    print("\n--- AUSENCIAS DETECTADAS ---")

    ausencias = detectar_ausencias(dia_semana, fecha)

    for a in ausencias:
        print(a.hora, a.aula, a.id_profesor_ausente)

    crear_guardias_desde_ausencias(ausencias, fecha)