from modules.db.db_manager import (
    obtener_horario_por_dia,
    obtener_presentes,
    crear_ausencia,
    crear_guardia,
    existe_guardia
)
from modules.presencia.registro import obtener_presentes_en_hora
from modules.guardias.reglas import ordenar_por_guardias
from modules.guardias.models import Guardia as GuardiaDominio


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
            ausencia = GuardiaDominio(
                hora=hora,
                aula=aula,
                id_profesor_ausente=profesor
            )

            ausencias.append(ausencia)

            crear_ausencia(profesor, fecha, hora)

    return ausencias


def crear_guardias_desde_ausencias(ausencias, fecha):
    for a in ausencias:
        if not existe_guardia(fecha, a.hora, a.aula):
            crear_guardia(
                fecha,
                a.hora,
                a.aula,
                a.id_profesor_ausente
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
    """
    Flujo principal:
    1. Detectar ausencias
    2. Crear guardias (sin duplicados)
    """

    ausencias = detectar_ausencias(dia_semana, fecha)
    crear_guardias_desde_ausencias(ausencias, fecha)

    print("\n--- AUSENCIAS DETECTADAS ---")
    for a in ausencias:
        print(a.hora, a.aula, a.id_profesor_ausente)

    crear_guardias_desde_ausencias(ausencias, fecha)