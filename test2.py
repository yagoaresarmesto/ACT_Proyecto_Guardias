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


FECHA = "2026-05-04"  # lunes
DIA_SEMANA = 1


def crear_datos_base():
    print("\n--- CREANDO DATOS BASE ---")

    nombres = ["Ana", "Luis", "Marta", "Carlos", "Elena", "Javier"]

    for nombre in nombres:
        crear_profesor(nombre)

    profesores = obtener_profesores()
    ids = {p.nombre: p.id_profesor for p in profesores}

    # Luis se crea aparte con horario completo para evitar duplicados.

    # Hora 1
    crear_horario(ids["Ana"], DIA_SEMANA, 1, "clase", "1ESO-A / Aula 101")
    crear_horario(ids["Marta"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Carlos"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Elena"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Javier"], DIA_SEMANA, 1, "clase", "2ESO-B / Aula 103")

    # Hora 2
    crear_horario(ids["Ana"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Marta"], DIA_SEMANA, 2, "clase", "3ESO-A / Aula 201")
    crear_horario(ids["Carlos"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Elena"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Javier"], DIA_SEMANA, 2, "clase", "4ESO-C / Aula 202")

    # Hora 3
    crear_horario(ids["Ana"], DIA_SEMANA, 3, "clase", "1BAC-A / Aula 301")
    crear_horario(ids["Marta"], DIA_SEMANA, 3, "clase", "2BAC-B / Aula 303")
    crear_horario(ids["Carlos"], DIA_SEMANA, 3, "clase", "FPB-1 / Aula 304")
    crear_horario(ids["Elena"], DIA_SEMANA, 3, "clase", "3ESO-C / Aula 305")
    crear_horario(ids["Javier"], DIA_SEMANA, 3, "clase", "FP2 / Aula 306")

    return ids


def crear_horario_completo_luis(ids):
    print("\n--- CREANDO HORARIO COMPLETO PARA LUIS ---")

    luis = ids["Luis"]

    horario_luis = {
        1: {
            1: ("clase", "1ESO-A / Aula 102"),
            2: ("clase", "2ESO-B / Aula 205"),
            3: ("guardia", "Guardia"),
            4: ("libre", None),
            5: ("clase", "3ESO-C / Aula 301"),
            6: ("clase", "4ESO-A / Aula 104"),
            7: ("libre", None),
            8: ("guardia", "Guardia"),
            9: ("libre", None),
            10: ("libre", None),
        },
        2: {
            1: ("guardia", "Guardia"),
            2: ("clase", "1BAC-A / Aula 210"),
            3: ("clase", "2ESO-A / Aula 203"),
            4: ("libre", None),
            5: ("clase", "3ESO-B / Aula 302"),
            6: ("guardia", "Guardia"),
            7: ("libre", None),
            8: ("libre", None),
            9: ("clase", "FPB-1 / Aula 401"),
            10: ("libre", None),
        },
        3: {
            1: ("clase", "4ESO-B / Aula 106"),
            2: ("libre", None),
            3: ("guardia", "Guardia"),
            4: ("clase", "1ESO-C / Aula 103"),
            5: ("clase", "2BAC-A / Aula 211"),
            6: ("libre", None),
            7: ("guardia", "Guardia"),
            8: ("libre", None),
            9: ("libre", None),
            10: ("clase", "FP2 / Aula 402"),
        },
        4: {
            1: ("libre", None),
            2: ("clase", "3ESO-A / Aula 300"),
            3: ("clase", "1BAC-B / Aula 212"),
            4: ("guardia", "Guardia"),
            5: ("libre", None),
            6: ("clase", "4ESO-C / Aula 107"),
            7: ("libre", None),
            8: ("guardia", "Guardia"),
            9: ("clase", "FP1 / Aula 403"),
            10: ("libre", None),
        },
        5: {
            1: ("clase", "2ESO-C / Aula 204"),
            2: ("guardia", "Guardia"),
            3: ("libre", None),
            4: ("clase", "1ESO-B / Aula 101"),
            5: ("clase", "3ESO-C / Aula 301"),
            6: ("libre", None),
            7: ("guardia", "Guardia"),
            8: ("libre", None),
            9: ("libre", None),
            10: ("libre", None),
        },
    }

    for dia_semana, horas in horario_luis.items():
        for hora, (tipo, aula) in horas.items():
            crear_horario(luis, dia_semana, hora, tipo, aula)

    print("Horario completo de Luis creado")


def crear_presencias(ids):
    print("\n--- CREANDO PRESENCIAS ---")

    registrar_evento(ids["Luis"], FECHA, 1, "entrada")
    registrar_evento(ids["Carlos"], FECHA, 1, "entrada")
    registrar_evento(ids["Elena"], FECHA, 1, "entrada")

    registrar_evento(ids["Marta"], FECHA, 1, "entrada")
    registrar_evento(ids["Marta"], FECHA, 2, "salida")


def preparar_ranking(ids):
    print("\n--- PREPARANDO CONTADORES PARA RANKING ---")

    sumar_guardia(ids["Carlos"])
    sumar_guardia(ids["Carlos"])

    sumar_guardia(ids["Elena"])


def mostrar_profesores():
    print("\n--- PROFESORES ---")
    for p in obtener_profesores():
        print(
            p.id_profesor,
            p.nombre,
            "semana:",
            p.guardias_semana,
            "acumuladas:",
            p.guardias_acumuladas,
        )


def probar_generacion_guardias():
    print("\n--- GENERANDO GUARDIAS ---")

    generar_guardias(DIA_SEMANA, FECHA)

    guardias = obtener_guardias(FECHA)

    print(f"\nTotal guardias generadas: {len(guardias)}")

    for g in guardias:
        print(
            f"Guardia {g.id_guardia} | "
            f"Hora {g.hora} | "
            f"Aula {g.aula} | "
            f"Ausente: {g.ausente_nombre} | "
            f"Cubre: {g.cubre_nombre}"
        )

    return guardias


def probar_rankings(guardias):
    print("\n--- RANKING POR GUARDIA ---")

    for g in guardias:
        ranking = obtener_ranking_guardia(DIA_SEMANA, FECHA, g.hora)

        print(f"Guardia {g.id_guardia} | Hora {g.hora} | Aula {g.aula}")
        print("Ranking IDs:", ranking)


def probar_asignacion(guardias):
    print("\n--- ASIGNANDO UNA GUARDIA ---")

    for g in guardias:
        ranking = obtener_ranking_guardia(DIA_SEMANA, FECHA, g.hora)

        if ranking:
            profesor_elegido = ranking[0]

            print(
                f"Asignando guardia {g.id_guardia} "
                f"al profesor ID {profesor_elegido}"
            )

            asignar_guardia(g.id_guardia, profesor_elegido)
            sumar_guardia(profesor_elegido)
            break

    guardias_actualizadas = obtener_guardias(FECHA)

    print("\n--- GUARDIAS TRAS ASIGNACIÓN ---")
    for g in guardias_actualizadas:
        print(
            f"Guardia {g.id_guardia} | "
            f"Hora {g.hora} | "
            f"Aula {g.aula} | "
            f"Ausente: {g.ausente_nombre} | "
            f"Cubre: {g.cubre_nombre}"
        )


def main():
    print("\n==============================")
    print("TEST CONTROLADO DEL PROYECTO")
    print("==============================")

    limpiar_bd_completa()

    ids = crear_datos_base()
    crear_horario_completo_luis(ids)
    crear_presencias(ids)
    preparar_ranking(ids)

    mostrar_profesores()

    guardias = probar_generacion_guardias()
    probar_rankings(guardias)

    # Actívalo solo si quieres probar asignación automática desde consola.
    # probar_asignacion(guardias)

    print("\n--- PROFESORES TRAS ASIGNACIÓN ---")
    mostrar_profesores()

    print("\nTEST FINALIZADO")


if __name__ == "__main__":
    main()