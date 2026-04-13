from db.db_manager import obtener_profesores, obtener_horarios


def ordenar_por_guardias(disponibles):
    profesores = obtener_profesores()
    horarios = obtener_horarios()

    carga = {}

    # Calculo de la carga lectiva
    for h in horarios:
        profesor_id = h[1]
        carga[profesor_id] = carga.get(profesor_id, 0) + 1

    # Filtrar solo los disponibles
    profesores_disponibles = [
        p for p in profesores if p[0] in disponibles
    ]

    # Ordenar por:
    # 1. guardias acumuladas
    # 2. guardias semana
    # 3. carga lectiva

    profesores_ordenados = sorted(
        profesores_disponibles,
        key=lambda p: (
            p[2],                      # guardias acumuladas
            p[3],                      # guardias semana
            carga.get(p[0], 0)         # carga lectiva
        )
    )

    return profesores_ordenados

#Ejemplo de orden:

'''
(0, 0, 2) → mejor
(0, 0, 3)
(0, 1, 1)
(1, 0, 1) → peor
'''