import random
from datetime import date, timedelta

from modules.db.db_manager import (
    crear_profesor, obtener_profesores,
    crear_horario,
    registrar_evento,
    obtener_guardias,
    limpiar_bd_completa,
    sumar_guardia
)

from modules.guardias.motor import generar_guardias


# -----------------------------
# CONFIG
# -----------------------------
NUM_PROFESORES = 15
DIAS_A_SIMULAR = 5
HORAS = list(range(1, 7))  # mañana


# -----------------------------
# GENERAR PROFESORES
# -----------------------------
def generar_profesores():
    print("\n--- GENERANDO PROFESORES ---")

    for i in range(NUM_PROFESORES):
        crear_profesor(f"Profesor {i+1}")

    print(f"{NUM_PROFESORES} profesores creados")


# -----------------------------
# GENERAR HORARIO ALEATORIO
# -----------------------------
def generar_horario():
    print("\n--- GENERANDO HORARIO ---")

    profesores = obtener_profesores()

    for p in profesores:
        for dia in range(1, 6):  # lunes a viernes
            for hora in HORAS:

                tipo = random.choice(["clase", "libre"])

                aula = f"Aula {random.randint(100, 110)}" if tipo == "clase" else None

                crear_horario(p.id_profesor, dia, hora, tipo, aula)

    print("Horario generado")


# -----------------------------
# GENERAR PRESENCIA REALISTA
# -----------------------------
def generar_presencia(fecha):
    print(f"\n--- GENERANDO PRESENCIA {fecha} ---")

    profesores = obtener_profesores()

    for p in profesores:

        # 80% probabilidad de ir al centro
        if random.random() < 0.8:

            hora_entrada = random.choice(HORAS)

            registrar_evento(p.id_profesor, fecha, hora_entrada, "entrada")

            # 50% probabilidad de salir
            if random.random() < 0.5:
                hora_salida = random.choice([h for h in HORAS if h >= hora_entrada])
                registrar_evento(p.id_profesor, fecha, hora_salida, "salida")

    print("Presencia generada")


# -----------------------------
# GENERAR GUARDIAS
# -----------------------------
def generar_guardias_dia(fecha):
    dia_semana = (date.fromisoformat(fecha).isoweekday())

    print(f"\n--- GENERANDO GUARDIAS {fecha} ---")

    generar_guardias(dia_semana, fecha)

    guardias = obtener_guardias(fecha)

    print(f"Total guardias: {len(guardias)}")

    for g in guardias[:5]:  # solo muestra 5 para no saturar
        print(g.aula, g.hora, g.ausente_nombre, g.cubre_nombre)


# -----------------------------
# SIMULACIÓN COMPLETA
# -----------------------------
def simulacion_completa():
    print("\n============================")
    print("SIMULACIÓN COMPLETA")
    print("============================")

    base = date(2026, 4, 20)

    for i in range(DIAS_A_SIMULAR):
        fecha = (base + timedelta(days=i)).isoformat()

        generar_presencia(fecha)
        generar_guardias_dia(fecha)


# -----------------------------
# EDGE CASES
# -----------------------------
def casos_extremos():
    print("\n--- CASOS EXTREMOS ---")

    fecha = "2026-05-01"

    profesores = obtener_profesores()

    # Nadie viene
    print("\nCaso: nadie presente")
    generar_guardias(1, fecha)
    print("Guardias:", len(obtener_guardias(fecha)))

    # Todos vienen pero nadie sale
    print("\nCaso: todos presentes sin salida")
    for p in profesores:
        registrar_evento(p.id_profesor, fecha, 1, "entrada")

    generar_guardias(1, fecha)
    print("Guardias:", len(obtener_guardias(fecha)))


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    limpiar_bd_completa()

    generar_profesores()
    generar_horario()

'''
    # ranking fake inicial
    for i in range(1, 6):
        sumar_guardia(i)

    simulacion_completa()

    casos_extremos()

'''