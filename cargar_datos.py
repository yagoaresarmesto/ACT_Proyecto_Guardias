from modules.db.db_manager import (
    limpiar_bd_completa,
    crear_profesor,
    obtener_profesores,
    crear_horario,
    registrar_evento,
    obtener_guardias,
    asignar_guardia,
    sumar_guardia,
)

from modules.guardias.motor import generar_guardias, obtener_ranking_guardia


FECHA = "2026-05-28"  # jueves
DIA_SEMANA = 4


def crear_profesores():
    nombres = [
        "Maria Jose Mosquera Garcia",
        "Luis Fernandez Castro",
        "Marta Alonso Rodriguez",
        "Carlos Perez Dominguez",
        "Elena Vazquez Lopez",
        "Javier Iglesias Santos",
        "Paula Rivas Martinez",
        "Diego Suarez Blanco",
        "Carmen Torres Pena",
        "Sergio Nunez Fernandez",
        "Raquel Prieto Gomez",
        "Andres Vidal Romero",
    ]

    for nombre in nombres:
        crear_profesor(nombre)

    return {p.nombre: p.id_profesor for p in obtener_profesores()}


def crear_horarios(ids):
    horarios = {
        "Maria Jose Mosquera Garcia": {
            1: ("clase", "1ESO-A / Aula 101"),
            2: ("clase", "2ESO-A / Aula 102"),
            3: ("libre", None),
            4: ("clase", "3ESO-B / Aula 201"),
            5: ("libre", None),
        },
        "Luis Fernandez Castro": {
            1: ("libre", None),
            2: ("clase", "1BAC-A / Aula 301"),
            3: ("libre", None),
            4: ("libre", None),
            5: ("clase", "2BAC-A / Aula 302"),
        },
        "Marta Alonso Rodriguez": {
            1: ("clase", "2ESO-B / Aula 103"),
            2: ("libre", None),
            3: ("clase", "4ESO-A / Aula 202"),
            4: ("clase", "1ESO-C / Aula 104"),
            5: ("libre", None),
        },
        "Carlos Perez Dominguez": {
            1: ("libre", None),
            2: ("libre", None),
            3: ("clase", "FPB-1 / Aula 401"),
            4: ("libre", None),
            5: ("clase", "2ESO-C / Aula 105"),
        },
        "Elena Vazquez Lopez": {
            1: ("clase", "3ESO-A / Aula 203"),
            2: ("clase", "1ESO-B / Aula 106"),
            3: ("libre", None),
            4: ("libre", None),
            5: ("libre", None),
        },
        "Javier Iglesias Santos": {
            1: ("clase", "4ESO-B / Aula 204"),
            2: ("clase", "2BAC-B / Aula 303"),
            3: ("clase", "1BAC-B / Aula 304"),
            4: ("libre", None),
            5: ("libre", None),
        },
        "Paula Rivas Martinez": {
            1: ("libre", None),
            2: ("clase", "1ESO-D / Aula 107"),
            3: ("libre", None),
            4: ("clase", "2ESO-D / Aula 108"),
            5: ("libre", None),
        },
        "Diego Suarez Blanco": {
            1: ("clase", "3ESO-C / Aula 205"),
            2: ("libre", None),
            3: ("libre", None),
            4: ("clase", "4ESO-C / Aula 206"),
            5: ("clase", "FP2 / Aula 402"),
        },
        "Carmen Torres Pena": {
            1: ("libre", None),
            2: ("libre", None),
            3: ("clase", "1ESO-E / Aula 109"),
            4: ("libre", None),
            5: ("clase", "2ESO-E / Aula 110"),
        },
        "Sergio Nunez Fernandez": {
            1: ("clase", "1BAC-C / Aula 305"),
            2: ("libre", None),
            3: ("clase", "2BAC-C / Aula 306"),
            4: ("libre", None),
            5: ("libre", None),
        },
        "Raquel Prieto Gomez": {
            1: ("libre", None),
            2: ("clase", "3ESO-D / Aula 207"),
            3: ("libre", None),
            4: ("clase", "4ESO-D / Aula 208"),
            5: ("libre", None),
        },
        "Andres Vidal Romero": {
            1: ("clase", "FP1 / Aula 403"),
            2: ("libre", None),
            3: ("clase", "FP2 / Aula 404"),
            4: ("libre", None),
            5: ("clase", "1ESO-F / Aula 111"),
        },
    }

    for nombre, horas in horarios.items():
        for hora, (tipo, aula) in horas.items():
            crear_horario(ids[nombre], DIA_SEMANA, hora, tipo, aula)


def crear_presencias(ids):
    presentes_hora_1 = [
        "Luis Fernandez Castro",
        "Carlos Perez Dominguez",
        "Elena Vazquez Lopez",
        "Paula Rivas Martinez",
        "Carmen Torres Pena",
        "Raquel Prieto Gomez",
    ]

    for nombre in presentes_hora_1:
        registrar_evento(ids[nombre], FECHA, 1, "entrada")

    # Marta entra y sale antes de 3ª hora: genera ausencia en hora 3 y 4.
    registrar_evento(ids["Marta Alonso Rodriguez"], FECHA, 1, "entrada")
    registrar_evento(ids["Marta Alonso Rodriguez"], FECHA, 2, "salida")

    # Sergio entra tarde: falta a 1ª, pero está presente desde 3ª.
    registrar_evento(ids["Sergio Nunez Fernandez"], FECHA, 3, "entrada")

    # Diego entra tarde: falta a 1ª, pero está presente en horas posteriores.
    registrar_evento(ids["Diego Suarez Blanco"], FECHA, 3, "entrada")

    # Ana/Mara, Javier y Andres no fichan: generan varias ausencias.


def preparar_ranking(ids):
    for _ in range(5):
        sumar_guardia(ids["Carlos Perez Dominguez"])

    for _ in range(3):
        sumar_guardia(ids["Elena Vazquez Lopez"])

    for _ in range(1):
        sumar_guardia(ids["Luis Fernandez Castro"])


def generar_guardias_demo():
    generar_guardias(DIA_SEMANA, FECHA)
    return obtener_guardias(FECHA)


def asignar_guardias_demo(guardias):
    """
    Deja mezcla de escenarios:
    - algunas guardias ya cubiertas
    - otras pendientes
    - horas 1 y 2 serán pasadas si HORA_TEST = 3
    """
    asignadas = 0

    for g in guardias:
        ranking = obtener_ranking_guardia(DIA_SEMANA, FECHA, g.hora)

        if ranking and asignadas < 3:
            profesor = ranking[0]
            asignar_guardia(g.id_guardia, profesor)
            sumar_guardia(profesor)
            asignadas += 1


def mostrar_resumen():
    print("\n--- PROFESORES ---")
    for p in obtener_profesores():
        print(
            p.id_profesor,
            p.nombre,
            "| semana:",
            p.guardias_semana,
            "| acumuladas:",
            p.guardias_acumuladas,
        )

    print("\n--- GUARDIAS ---")
    for g in obtener_guardias(FECHA):
        print(
            f"Guardia {g.id_guardia} | "
            f"Hora {g.hora} | "
            f"Aula: {g.aula} | "
            f"Ausente: {g.ausente_nombre} | "
            f"Cubre: {g.cubre_nombre}"
        )


def main():
    print("CARGANDO DATOS DEMO")
    print(f"Fecha demo: {FECHA}")

    limpiar_bd_completa()

    ids = crear_profesores()
    crear_horarios(ids)
    crear_presencias(ids)
    preparar_ranking(ids)

    guardias = generar_guardias_demo()
    asignar_guardias_demo(guardias)

    mostrar_resumen()

    print("DATOS DEMO CARGADOS")
    print("Recomendado en config.py:")
    print('MODO_TEST = True')
    print('FECHA_TEST = "2026-05-28"')
    print("HORA_TEST = 3")


if __name__ == "__main__":
    main()