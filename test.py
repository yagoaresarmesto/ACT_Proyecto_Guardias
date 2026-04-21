from modules.db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario, obtener_horario,
    registrar_presencia, obtener_presencia,
    obtener_guardias,
    limpiar_bd_completa,sumar_guardia
)

from modules.guardias.motor import generar_guardias
from modules.guardias.reglas import ordenar_por_guardias

def test_profesores():
    crear_profesor("Profesor 1")
    crear_profesor("Profesor 2")
    crear_profesor("Profesor 3")
    crear_profesor("Profesor 4")
    crear_profesor("Profesor 5")

    print("\nProfesores:")
    for p in obtener_profesores():
        print(dict(p))


def test_horario():
    # Lunes = 1

    # Hora 1
    crear_horario(1, 1, 1, "clase", "Aula 101")
    crear_horario(2, 1, 1, "clase", "Aula 102")

    # Hora 2
    crear_horario(3, 1, 2, "clase", "Aula 103")
    crear_horario(4, 1, 2, "clase", "Aula 104")

    # Hora 3
    crear_horario(5, 1, 3, "clase", "Aula 105")

    print("\nHorario:")
    for h in obtener_horario():
        print(dict(h))


def test_presencia():
    fecha = "2026-04-20"

    # Presentes por hora
    registrar_presencia(1, fecha, 1)
    registrar_presencia(1, fecha, 2)
    registrar_presencia(1, fecha, 3)

    registrar_presencia(3, fecha, 1)
    registrar_presencia(3, fecha, 2)
    registrar_presencia(3, fecha, 3)

    print("\nPresencia:")
    for p in obtener_presencia(fecha):
        print(dict(p))


def test_generar_guardias():
    fecha = "2026-04-20"
    dia = 1  # Lunes

    print("\n--- GENERANDO GUARDIAS ---")
    generar_guardias(dia, fecha)

    print("\nGuardias:")
    guardias = obtener_guardias(fecha)

    for g in guardias:
        print(dict(g))

def test_ranking():
    print("\n--- TEST RANKING ---")

    # Simular que profesor 1 ya tiene guardias
    sumar_guardia(1)
    sumar_guardia(1)

    sumar_guardia(2)

    disponibles = {1, 2, 3}

    ranking = ordenar_por_guardias(disponibles)

    print("Ranking esperado: 3 primero (menos guardias)")
    print("Resultado:", ranking)


def test_limpiar_bd():
    limpiar_bd_completa()
    print("\nBase de datos limpiada")


if __name__ == "__main__":
    test_limpiar_bd()

    test_profesores()
    test_horario()
    test_presencia()

    test_ranking()
    test_generar_guardias()
