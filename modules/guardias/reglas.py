from modules.db.db_manager import obtener_profesores

def ordenar_por_guardias(profesores_ids):
    """
    Ordena profesores por menor número de guardias acumuladas.
    Desempata por id_profesor para mantener consistencia.
    """

    if not profesores_ids:
        return []

    profesores = obtener_profesores()

    # Filtrar solo los profesores disponibles
    profesores_filtrados = [
        p for p in profesores if p["id_profesor"] in profesores_ids
    ]

    # Ordenar:
    # 1. Menos guardias acumuladas
    # 2. Menor id (desempate estable)
    profesores_ordenados = sorted(
        profesores_filtrados,
        key=lambda p: (p["guardias_acumuladas"], p["id_profesor"])
    )

    # Devolver solo ID
    return [p["id_profesor"] for p in profesores_ordenados]