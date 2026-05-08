from modules.db.db_manager import (
    obtener_profesores,
    obtener_horario
)

from modules.guardias.models import ProfesorDisponible

def calcular_carga_lectiva():
    horario = obtener_horario()
    carga = {}

    for h in horario:
        if h["tipo"] != "clase":
            continue

        profesor_id = h["id_profesor"]

        if profesor_id not in carga:
            carga[profesor_id] = 0

        carga[profesor_id] += 1

    return carga

def construir_profesores_disponibles(profesores_ids):
    profesores = obtener_profesores()
    carga_lectiva = calcular_carga_lectiva()

    disponibles = []

    for p in profesores:
        if p.id_profesor not in profesores_ids:
            continue

        disponible = ProfesorDisponible(
            id_profesor=p.id_profesor,
            guardias_acumuladas=p.guardias_acumuladas,
            guardias_semana=p.guardias_semana,
            carga_lectiva=carga_lectiva.get(p.id_profesor, 0)
        )

        disponibles.append(disponible)

    return disponibles

def ordenar_por_guardias(profesores_ids):
    """
    Ordena profesores según:
    1. guardias acumuladas
    2. guardias en la semana
    3. carga lectiva
    4. id (en caso de empate)
    """

    if not profesores_ids:
        return []

    disponibles = construir_profesores_disponibles(profesores_ids)

    disponibles_ordenados = sorted(
        disponibles,
        key=lambda p: (
            p.guardias_acumuladas,
            p.guardias_semana,
            p.carga_lectiva,
            p.id_profesor
        )
    )

    return [p.id_profesor for p in disponibles_ordenados]