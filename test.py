# IMPORTS
from db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario, obtener_horarios,
    registrar_entrada, obtener_presencia,
    obtener_ausentes
)

from modules.guardias.motor import (
    obtener_aulas_sin_profesor,
    obtener_profesores_disponibles,
    asignar_guardias
)

from modules.guardias.reglas import ordenar_por_guardias


# PRUEBAS DB

def test_profesores():
    crear_profesor("Profesor 1")
    crear_profesor("Profesor 2")
    crear_profesor("Profesor 3")
    crear_profesor("Profesor 4")
    crear_profesor("Profesor 5")

    print(obtener_profesores())


def test_horarios():
    crear_horario(1, "Lunes", 1, "Aula 101")
    crear_horario(2, "Lunes", 1, "Aula 102")

    crear_horario(3, "Lunes", 2, "Aula 103")
    crear_horario(4, "Lunes", 2, "Aula 104")

    crear_horario(5, "Lunes", 3, "Aula 105")

    print(obtener_horarios())


def test_presencia():
    # Presentes
    registrar_entrada(1, "2026-04-09", "08:00")
    registrar_entrada(3, "2026-04-09", "08:05")
    # registrar_entrada(5, "2026-04-09", "08:10")

    # Ausentes → 2 y 4

    print(obtener_presencia())


def test_ausencias():
    print(obtener_ausentes("Lunes", "2026-04-09"))


# MOTOR

def test_aulas():
    print(obtener_aulas_sin_profesor("Lunes", "2026-04-09"))


def test_disponibles():
    print(obtener_profesores_disponibles("Lunes", 2, "2026-04-09"))


# REGLAS


def test_reglas():
    disponibles = obtener_profesores_disponibles("Lunes", 2, "2026-04-09")
    print(ordenar_por_guardias(disponibles))



def test_asignacion():
    resultado = asignar_guardias("Lunes", "2026-04-09")
    print(resultado)


def test_limpiar_bd():
    from db.db_manager import limpiar_bd_completa

    limpiar_bd_completa()
    print("Base de datos limpiada")

if __name__ == "__main__":
    test_limpiar_bd()
    test_profesores()
    test_horarios()
    test_presencia()
    # test_ausencias()

    #test_aulas()
    # test_disponibles()

    #test_reglas()
    test_asignacion()