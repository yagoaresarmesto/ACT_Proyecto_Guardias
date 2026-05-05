from modules.db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario, obtener_horario,
    registrar_evento, obtener_eventos,
    obtener_presentes,
    obtener_guardias,
    limpiar_bd_completa, sumar_guardia
)

from modules.guardias.motor import generar_guardias
from modules.guardias.reglas import ordenar_por_guardias


# -----------------------------
# PROFESORES
# -----------------------------
def test_profesores():
    crear_profesor("Yago Ares")
    crear_profesor("Jesús Ares")
    crear_profesor("Ana Armesto")
    crear_profesor("Gabriel Montes")
    crear_profesor("Fernando Sierra")

    print("\nProfesores:")
    for p in obtener_profesores():
        print(p.id_profesor, p.nombre, p.guardias_acumuladas)


# -----------------------------
# HORARIO
# -----------------------------
def test_horario():
    crear_horario(1, 1, 1, "clase", "Aula 101")
    crear_horario(2, 1, 1, "clase", "Aula 102")

    crear_horario(3, 1, 1, "libre", None)
    crear_horario(4, 1, 1, "libre", None)
    crear_horario(5, 1, 1, "libre", None)

    print("\nHorario:")
    for h in obtener_horario():
        print(dict(h))


# -----------------------------
# PRESENCIA (NUEVO MODELO)
# -----------------------------
def test_presencia_eventos():
    fecha = "2026-04-20"

    print("\n--- EVENTOS PRESENCIA ---")

    # Profesor 1 entra en hora 1
    registrar_evento(1, fecha, 1, "entrada")

    # Profesor 1 sale en hora 3
    registrar_evento(1, fecha, 3, "salida")

    # Profesor 3 entra y no sale
    registrar_evento(3, fecha, 1, "entrada")

    eventos = obtener_eventos(fecha)

    for e in eventos:
        print(dict(e))

    presentes = obtener_presentes(fecha)
    print("Presentes actualmente:", presentes)


# -----------------------------
# RANKING
# -----------------------------
def preparar_ranking_real():
    print("\n--- PREPARANDO RANKING REAL ---")

    sumar_guardia(4)
    sumar_guardia(5)
    sumar_guardia(5)


def test_ranking():
    print("\n--- TEST RANKING ---")

    sumar_guardia(1)
    sumar_guardia(1)
    sumar_guardia(2)

    disponibles = {1, 2, 3}

    ranking = ordenar_por_guardias(disponibles)

    print("Ranking esperado: 3 primero (menos guardias)")
    print("Resultado:", ranking)


# -----------------------------
# ESCENARIOS
# -----------------------------
def escenario_todos_presentes():
    print("\n--- ESCENARIO: TODOS PRESENTES ---")

    fecha = "2026-04-21"

    for p in range(1, 6):
        registrar_evento(p, fecha, 1, "entrada")

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

    # Profesor 1 entra pero está en clase
    registrar_evento(1, fecha, 1, "entrada")

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
        registrar_evento(p, fecha, 1, "entrada")

    generar_guardias(1, fecha)

    guardias = obtener_guardias(fecha)

    for g in guardias:
        print(g.aula, g.cubre_nombre)


# -----------------------------
# LIMPIEZA
# -----------------------------
def test_limpiar_bd():
    limpiar_bd_completa()
    print("\nBase de datos limpiada")


# -----------------------------
# MAIN
# -----------------------------
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

    test_presencia_eventos()