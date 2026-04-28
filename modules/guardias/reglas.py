from modules.db.db_manager import (
    obtener_profesores,
    obtener_horario
)

#Calculo para la carga lectiva
def calcular_carga_lectiva():
    """
    Devuelve un diccionario:
    {id_profesor: numero_de_clases}
    """

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


def ordenar_por_guardias(profesores_ids):
    """
    Ordena profesores según:
    1. guardias acumuladas
    2. guardias en la semana
    3. carga lectiva
    4. id (desempate final)
    """

    if not profesores_ids:
        return []

    profesores = obtener_profesores()
    carga_lectiva = calcular_carga_lectiva()

    profesores_filtrados = [
        p for p in profesores if p.id_profesor in profesores_ids
    ]

    profesores_ordenados = sorted(
        profesores_filtrados,
        key=lambda p: (
            p.guardias_acumuladas,
            p.guardias_semana,
            carga_lectiva.get(p.id_profesor, 0),
            p.id_profesor
        )
    )

    return [p.id_profesor for p in profesores_ordenados]