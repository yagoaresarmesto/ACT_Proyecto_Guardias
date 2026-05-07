from datetime import date, timedelta

from modules.db.db_manager import (
    obtener_horario_profesor,
    obtener_guardias_profesor_entre_fechas,
)


DIAS = {
    1: "L",
    2: "M",
    3: "X",
    4: "J",
    5: "V",
}

HORAS = list(range(1, 11))


def obtener_inicio_fin_semana(fecha):
    fecha_obj = date.fromisoformat(fecha)

    inicio_semana = fecha_obj - timedelta(days=fecha_obj.isoweekday() - 1)
    fin_semana = inicio_semana + timedelta(days=4)

    return inicio_semana.isoformat(), fin_semana.isoformat()


def construir_tabla_horario(id_profesor, fecha):
    horario = obtener_horario_profesor(id_profesor)

    fecha_inicio, fecha_fin = obtener_inicio_fin_semana(fecha)

    guardias = obtener_guardias_profesor_entre_fechas(
        id_profesor,
        fecha_inicio,
        fecha_fin
    )

    tabla = {
        hora: {
            dia: ""
            for dia in DIAS
        }
        for hora in HORAS
    }

    # 1. Horario fijo semanal
    for h in horario:
        dia = h["dia_semana"]
        hora = h["hora"]
        tipo = h["tipo"]
        aula = h["aula"]

        if hora not in tabla or dia not in DIAS:
            continue

        if tipo == "clase":
            tabla[hora][dia] = aula or "Clase"
        elif tipo == "guardia":
            tabla[hora][dia] = aula or "Guardia"
        else:
            tabla[hora][dia] = ""

    # 2. Guardias reales asignadas esa semana
    for g in guardias:
        fecha_guardia = date.fromisoformat(g.fecha)
        dia = fecha_guardia.isoweekday()
        hora = g.hora

        if hora not in tabla or dia not in DIAS:
            continue

        tabla[hora][dia] = f"Guardia real: {g.aula}"

    return tabla, fecha_inicio, fecha_fin