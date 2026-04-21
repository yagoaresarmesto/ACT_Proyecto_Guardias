from modules.db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario, obtener_horario,
    registrar_presencia, obtener_presencia,
    obtener_guardias,
    limpiar_bd_completa, sumar_guardia
)

from modules.guardias.motor import generar_guardias
from modules.guardias.reglas import ordenar_por_guardias


def test_profesores():
    crear_profesor("Yago Ares")
    crear_profesor("Jesús Ares")
    crear_profesor("Ana Armesto")
    crear_profesor("Gabriel Montes")
    crear_profesor("Fernando Sierra")

    print("\nProfesores:")
    for p in obtener_profesores():
        print(p.id_profesor, p.nombre, p.guardias_acumuladas)


def test_horario():
    crear_horario(1, 1, 1, "clase", "Aula 101")
    crear_horario(2, 1, 1, "clase", "Aula 102")

    crear_horario(3, 1, 1, "libre", None)
    crear_horario(4, 1, 1, "libre", None)
    crear_horario(5, 1, 1, "libre", None)

    print("\nHorario:")
    for h in obtener_horario():
        print(dict(h))  # 👈 este lo puedes dejar (no lo has modelado)


def test_presencia():
    fecha = "2026-04-20"

    presentes = [1, 3, 4, 5]

    for p in presentes:
        registrar_presencia(p, fecha, 1)

    print("\nPresencia:")
    for p in obtener_presencia(fecha):
        print(dict(p))  # 👈 sigue siendo Row


def preparar_ranking_real():
    print("\n--- PREPARANDO RANKING REAL ---")

    sumar_guardia(4)
    sumar_guardia(5)
    sumar_guardia(5)


def test_generar_guardias():
    fecha = "2026-04-20"
    dia = 1

    print("\n--- GENERANDO GUARDIAS ---")
    generar_guardias(dia, fecha)

    print("\nGuardias:")
    guardias = obtener_guardias(fecha)

    for g in guardias:
        print(
            g.id_guardia,
            g.aula,
            g.hora,
            g.ausente_nombre,
            g.cubre_nombre
        )


def test_ranking():
    print("\n--- TEST RANKING ---")

    sumar_guardia(1)
    sumar_guardia(1)
    sumar_guardia(2)

    disponibles = {1, 2, 3}

    ranking = ordenar_por_guardias(disponibles)

    print("Ranking esperado: 3 primero (menos guardias)")
    print("Resultado:", ranking)


def escenario_todos_presentes():
    print("\n--- ESCENARIO: TODOS PRESENTES ---")

    fecha = "2026-04-21"

    for p in range(1, 6):
        for h in range(1, 4):
            registrar_presencia(p, fecha, h)

    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    print("Guardias esperadas: 0")
    print("Resultado:", len(guardias))


def escenario_todos_ausentes():
    print("\n--- ESCENARIO: TODOS AUSENTES ---")

    fecha = "2026-04-22"

    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    print("Guardias generadas:", len(guardias))

    for g in guardias:
        print(g.aula, g.hora)


def escenario_ocupados_no_disponibles():
    print("\n--- ESCENARIO: PRESENTE PERO OCUPADO ---")

    fecha = "2026-04-23"

    registrar_presencia(1, fecha, 1)

    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    for g in guardias:
        print(g.aula, g.hora, g.cubre_nombre)


def escenario_evitar_duplicados():
    print("\n--- ESCENARIO: NO DUPLICAR GUARDIAS ---")

    fecha = "2026-04-24"

    generar_guardias(1, fecha)
    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    print("Total guardias:", len(guardias))


def escenario_empate_ranking():
    print("\n--- ESCENARIO: EMPATE EN RANKING ---")

    fecha = "2026-04-25"

    for p in [1, 2, 3]:
        registrar_presencia(p, fecha, 1)

    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    for g in guardias:
        print(g.aula, g.cubre_nombre)


def test_limpiar_bd():
    limpiar_bd_completa()
    print("\nBase de datos limpiada")


if __name__ == "__main__":
    test_limpiar_bd()

    test_profesores()
    test_horario()

    preparar_ranking_real()

    test_ranking()

    escenario_todos_presentes()
    escenario_todos_ausentes()
    escenario_ocupados_no_disponibles()
    escenario_evitar_duplicados()
    escenario_empate_ranking()

    test_presencia()
    test_generar_guardias()