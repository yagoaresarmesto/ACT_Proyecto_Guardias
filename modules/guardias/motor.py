from modules.db.db_manager import (
    obtener_horario_por_dia,
    obtener_presentes,
    crear_ausencia,
    crear_guardia,
    existe_guardia,
    obtener_profesores_asignados
)

from modules.utils.tiempo import obtener_hora_lectiva_actual
from modules.guardias.reglas import ordenar_por_guardias
from modules.guardias.models import Guardia as GuardiaDominio

from datetime import date


# DETECTAR AUSENCIAS
def detectar_ausencias(dia_semana, fecha):
    horario = obtener_horario_por_dia(dia_semana)
    ausencias = []

    for h in horario:
        if h["tipo"] != "clase":
            continue

        hora = h["hora"]
        profesor = h["id_profesor"]
        aula = h["aula"]

        presentes = obtener_presentes(fecha)

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


# DISPONIBLES (FIX COMPLETO)
def obtener_disponibles(dia_semana, fecha, hora):
    horario = obtener_horario_por_dia(dia_semana)
    presentes = obtener_presentes(fecha)

    hoy = date.today().isoformat()

    if fecha == hoy:
        hora_actual = obtener_hora_lectiva_actual()
        if hora_actual and hora < hora_actual:
            return set()

    ocupados = {
        h["id_profesor"]
        for h in horario
        if h["hora"] == hora and h["tipo"] == "clase"
    }

    # Profesores ya asignados a guardias
    asignados = obtener_profesores_asignados(fecha, hora)

    disponibles = presentes - ocupados - asignados

    return disponibles


# RANKING
def obtener_ranking_guardia(dia_semana, fecha, hora):
    disponibles = obtener_disponibles(dia_semana, fecha, hora)

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