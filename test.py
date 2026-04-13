# IMPORTS
from db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario, obtener_horarios,
    registrar_entrada, obtener_presencia,
    obtener_ausentes
)

from modules.guardias.motor import (
    obtener_aulas_sin_profesor,
    obtener_profesores_disponibles
)

from modules.guardias.reglas import ordenar_por_guardias


# PRUEBAS DB

def test_profesores():
    crear_profesor("Yago Ares Armesto")
    crear_profesor("Jesus Ares Armesto")
    print(obtener_profesores())


def test_horarios():
    crear_horario(1, "Lunes", 1, "Aula 238")
    crear_horario(4, "Lunes", 2, "Aula 239")
    print(obtener_horarios())


def test_presencia():
    registrar_entrada(1, "2026-04-09", "08:00")
    registrar_entrada(2, "2026-04-09", "08:05")
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


if __name__ == "__main__":
    # Activa SOLO lo que quieras probar:

    # test_profesores()
    # test_horarios()
    # test_presencia()
    # test_ausencias()

    # test_aulas()
    # test_disponibles()

    test_reglas()