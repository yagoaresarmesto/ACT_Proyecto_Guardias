from db.db_manager import obtener_profesores


def ordenar_por_guardias(disponibles):
    profesores = obtener_profesores()

    # Filtrar solo los disponibles
    profesores_disponibles = [p for p in profesores if p[0] in disponibles]

    # Ordenar por guardias_acumuladas, que es el campo 2
    profesores_ordenadas = sorted(
        profesores_disponibles, key = lambda p: p[2]
    )

    return profesores_ordenadas