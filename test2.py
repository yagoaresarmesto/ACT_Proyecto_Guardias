from datetime import date

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

    nombres = [
        "Ana",
        "Luis",
        "Marta",
        "Carlos",
        "Elena",
        "Javier",
    ]

    for nombre in nombres:
        crear_profesor(nombre)

    profesores = obtener_profesores()
    ids = {p.nombre: p.id_profesor for p in profesores}

    # Hora 1:
    # Ana y Luis tienen clase. Ana no viene -> genera guardia.
    # Marta, Carlos y Elena están libres y pueden cubrir.
    crear_horario(ids["Ana"], DIA_SEMANA, 1, "clase", "Aula 101")
    crear_horario(ids["Luis"], DIA_SEMANA, 1, "clase", "Aula 102")
    crear_horario(ids["Marta"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Carlos"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Elena"], DIA_SEMANA, 1, "libre")
    crear_horario(ids["Javier"], DIA_SEMANA, 1, "clase", "Aula 103")

    # Hora 2:
    # Marta tiene clase y no viene -> genera guardia.
    # Luis, Carlos y Elena podrían cubrir.
    crear_horario(ids["Ana"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Luis"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Marta"], DIA_SEMANA, 2, "clase", "Aula 201")
    crear_horario(ids["Carlos"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Elena"], DIA_SEMANA, 2, "libre")
    crear_horario(ids["Javier"], DIA_SEMANA, 2, "clase", "Aula 202")

    # Hora 3:
    # Todos los presentes tienen clase o están ausentes -> sin disponibles.
    crear_horario(ids["Ana"], DIA_SEMANA, 3, "clase", "Aula 301")
    crear_horario(ids["Luis"], DIA_SEMANA, 3, "clase", "Aula 302")
    crear_horario(ids["Marta"], DIA_SEMANA, 3, "clase", "Aula 303")
    crear_horario(ids["Carlos"], DIA_SEMANA, 3, "clase", "Aula 304")
    crear_horario(ids["Elena"], DIA_SEMANA, 3, "clase", "Aula 305")
    crear_horario(ids["Javier"], DIA_SEMANA, 3, "clase", "Aula 306")

    return ids


def crear_presencias(ids):
    print("\n--- CREANDO PRESENCIAS ---")

    # Ana no ficha: ausente.
    # Marta ficha entrada y salida: termina ausente.
    # Javier no ficha: ausente.
    # Luis, Carlos y Elena están presentes.

    registrar_evento(ids["Luis"], FECHA, 1, "entrada")
    registrar_evento(ids["Carlos"], FECHA, 1, "entrada")
    registrar_evento(ids["Elena"], FECHA, 1, "entrada")

    registrar_evento(ids["Marta"], FECHA, 1, "entrada")
    registrar_evento(ids["Marta"], FECHA, 2, "salida")


def preparar_ranking(ids):
    print("\n--- PREPARANDO CONTADORES PARA RANKING ---")

    # Carlos queda con más guardias acumuladas.
    sumar_guardia(ids["Carlos"])
    sumar_guardia(ids["Carlos"])

    # Elena queda con una guardia acumulada.
    sumar_guardia(ids["Elena"])

    # Luis queda con cero guardias, debería priorizarse si está disponible.


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
    crear_presencias(ids)
    preparar_ranking(ids)

    mostrar_profesores()

    guardias = probar_generacion_guardias()
    probar_rankings(guardias)
    #probar_asignacion(guardias)

    print("\n--- PROFESORES TRAS ASIGNACIÓN ---")
    mostrar_profesores()

    print("\nTEST FINALIZADO")


if __name__ == "__main__":
    main()