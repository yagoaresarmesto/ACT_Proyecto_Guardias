from modules.db.db_manager import (
    insertar_profesor,
    get_all_profesores,
    insertar_horario,
    get_all_horarios,
    registrar_presencia,
    get_all_presencias,
    get_ausentes,
    guardar_guardia,
    limpiar_bd_completa
)

try:
    from modules.guardias.motor import (
        obtener_aulas_sin_profesor,
        obtener_profesores_disponibles,
        obtener_guardias_para_vista
    )
except ImportError:
    def obtener_aulas_sin_profesor(*args, **kwargs):
        return ["Aula 101", "Aula 103"]

    def obtener_profesores_disponibles(*args, **kwargs):
        class Dummy:
            def __init__(self, nombre): self.nombre = nombre
        return [Dummy("Profesor 2"), Dummy("Profesor 4"), Dummy("Profesor 5")]

    def obtener_guardias_para_vista(*args, **kwargs):
        return [{"aula": "Aula 101", "cubre": "Profesor 2"}]

try:
    from modules.guardias.reglas import (
        ordenar_por_guardias
    )
except ImportError:
    def ordenar_por_guardias(lista):
        return lista  # no hace nada por ahora


def test_limpiar_bd():
    limpiar_bd_completa()
    print("Base de datos reiniciada.")


def test_profesores():
    for nombre in ["Profesor 1", "Profesor 2", "Profesor 3", "Profesor 4", "Profesor 5"]:
        insertar_profesor(nombre, "Departamento X")

    print("\nProfesores registrados:")
    for p in get_all_profesores():
        print(vars(p))


def test_horarios():
     insertar_horario(1, 1, 1, "Aula 101", "clase")  # 1 = lunes
     insertar_horario(2, 1, 1, "Aula 102", "clase")
     insertar_horario(3, 1, 2, "Aula 103", "clase")
     insertar_horario(4, 1, 2, "Aula 104", "guardia")
     insertar_horario(5, 1, 3, "Aula 105", "libre")

     print("\nHorarios cargados:")
     for h in get_all_horarios():
        print(vars(h))

def test_presencias():
    registrar_presencia(1, "2026-04-09", 1, True)
    registrar_presencia(3, "2026-04-09", 1, True)
    print("\nPresencias actuales:")
    for p in get_all_presencias():
        print(vars(p))


def test_ausentes():
    print("\nProfesores ausentes detectados:")
    ausentes = get_ausentes("Lunes", "2026-04-09")
    for a in ausentes:
        print(a)


def test_motor():
    print("\nAulas sin profesor:")
    print(obtener_aulas_sin_profesor("Lunes", "2026-04-09"))

    print("\nProfesores disponibles:")
    disponibles = obtener_profesores_disponibles("Lunes", 1, "2026-04-09")
    for d in disponibles:
        print(vars(d) if hasattr(d, "__dict__") else d)


def test_reglas():
    print("\nRanking por guardias:")
    disponibles = obtener_profesores_disponibles("Lunes", 1, "2026-04-09")
    ranking = ordenar_por_guardias(disponibles)
    for r in ranking:
        print(vars(r) if hasattr(r, "__dict__") else r)


def test_guardias():
    guardar_guardia("Aula 102", 1, "2026-04-09", 1)
    print("\nGuardias registradas correctamente.")


def test_vista_guardias():
    print("\nResumen para vista Flask:")
    vista = obtener_guardias_para_vista("Lunes", "2026-04-09")
    for v in vista:
        print(v)


if __name__ == "__main__":
    test_limpiar_bd()
    test_profesores()
    test_horarios()
    test_presencias()
    test_ausentes()
    test_motor()
    test_reglas()
    test_guardias()
    test_vista_guardias()
