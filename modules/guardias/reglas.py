from db.db_manager import obtener_profesores


def ordenar_por_guardias(disponibles):
    profesores = obtener_profesores()

    # Filtrar solo los disponibles
    profesores_disponibles = [
        p for p in profesores if p[0] in disponibles
    ]

    # Ordenar por:
    # 1. guardias_acumuladas
    # 2. guardias_semana
    profesores_ordenados = sorted(
        profesores_disponibles,
        key=lambda p: (p[2], p[3])
    )

    return profesores_ordenados

#por ejemplo:
'''
(0,0) → mejor
(0,1)
(1,0)
(1,1) → peor
'''
