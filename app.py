from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

from modules.guardias.motor import generar_guardias, obtener_ranking_guardia
from modules.db.db_manager import (
    obtener_guardias,
    asignar_guardia,
    sumar_guardia,
    obtener_profesores,
)

from modules.presencia.registro import obtener_presencia_dia, registrar_evento
from modules.horarios.servicio import construir_tabla_horario, DIAS, HORAS
from modules.utils.tiempo import obtener_hora_lectiva_actual

app = Flask(__name__)


# CONFIGURACIÓN MODO TEST / REAL


MODO_TEST = False

# Solo se usan si MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 2
# Si MODO_TEST = False, se usa fecha real y hora real lectiva


TRAMOS_HORARIOS = {
    1: ("08:50", "09:40"),
    2: ("09:40", "10:30"),
    3: ("10:30", "11:20"),
    4: ("11:40", "12:30"),
    5: ("12:30", "13:20"),
    6: ("13:20", "14:10"),
    7: ("16:00", "17:00"),
    8: ("17:00", "18:00"),
    9: ("18:00", "19:00"),
    10: ("19:00", "20:00"),
}


def obtener_tramo_hora(hora):
    tramo = TRAMOS_HORARIOS.get(hora)
    return f"{tramo[0]} - {tramo[1]}" if tramo else ""


def obtener_fecha_actual_app():
    if MODO_TEST:
        return FECHA_TEST
    return date.today().isoformat()


def obtener_hora_actual_app():
    if MODO_TEST:
        return HORA_TEST
    return obtener_hora_lectiva_actual()


def obtener_hora_real_app():
    return datetime.now().strftime("%H:%M")


def guardia_esta_pasada(guardia, fecha):
    fecha_actual = obtener_fecha_actual_app()
    hora_actual = obtener_hora_actual_app()

    es_fecha_pasada = fecha < fecha_actual

    es_fuera_de_horario = (
        fecha == fecha_actual
        and hora_actual is None
    )

    es_hora_pasada = (
        fecha == fecha_actual
        and hora_actual is not None
        and guardia.hora < hora_actual
    )

    return es_fecha_pasada or es_fuera_de_horario or es_hora_pasada


@app.route("/")
def index():
    return render_template("index.html")

# GUARDIAS

@app.route("/guardias")
def vista_guardias():
    fecha = request.args.get("fecha", obtener_fecha_actual_app())
    hora_real = obtener_hora_real_app()
    dia_semana = datetime.fromisoformat(fecha).isoweekday()
    hora_actual = obtener_hora_actual_app()
    fecha_actual = obtener_fecha_actual_app()

    generar_guardias(dia_semana, fecha)
    guardias = obtener_guardias(fecha)

    ranking_por_guardia = {}

    for g in guardias:
        if guardia_esta_pasada(g, fecha) or g.id_profesor_cubre:
            ranking_por_guardia[g.id_guardia] = []
        else:
            ranking_por_guardia[g.id_guardia] = obtener_ranking_guardia(
                dia_semana,
                fecha,
                g.hora,
                hora_actual
            )

    profesores = obtener_profesores()

    profesores_dict = {
        p.id_profesor: p.nombre
        for p in profesores
    }

    return render_template(
        "vista_guardias.html",
        guardias=guardias,
        fecha=fecha,
        ranking_por_guardia=ranking_por_guardia,
        profesores_dict=profesores_dict,
        obtener_tramo_hora=obtener_tramo_hora,
        hora_actual=hora_actual,
        fecha_actual=fecha_actual,
        hora_real=hora_real,
    )


@app.route("/asignar_guardia", methods=["POST"])
def asignar_guardia_manual():
    id_guardia = int(request.form["id_guardia"])
    profesor_id = request.form.get("profesor_id")
    fecha = request.form.get("fecha")

    if not profesor_id:
        return redirect(url_for("vista_guardias", fecha=fecha))

    guardias = obtener_guardias(fecha)
    guardia = next((g for g in guardias if g.id_guardia == id_guardia), None)

    if not guardia:
        return redirect(url_for("vista_guardias", fecha=fecha))

    if guardia.id_profesor_cubre:
        return redirect(url_for("vista_guardias", fecha=fecha))

    if guardia_esta_pasada(guardia, fecha):
        return redirect(url_for("vista_guardias", fecha=fecha))

    profesor_id = int(profesor_id)

    asignar_guardia(id_guardia, profesor_id)
    sumar_guardia(profesor_id)

    return redirect(url_for("vista_guardias", fecha=fecha))


# =============================
# PRESENCIA
# =============================

@app.route("/presencia", methods=["GET", "POST"])
def vista_presencia():
    fecha = (
        request.form.get("fecha")
        or request.args.get("fecha")
        or obtener_fecha_actual_app()
    )

    hora_real = obtener_hora_real_app()
    hora_lectiva = obtener_hora_actual_app()

    if request.method == "POST":
        profesor_id = request.form.get("profesor_id")

        if not profesor_id:
            return redirect(url_for("vista_presencia", fecha=fecha))

        if hora_lectiva is None:
            return redirect(url_for("vista_presencia", fecha=fecha))

        registrar_evento(int(profesor_id), fecha, hora_lectiva)

        return redirect(url_for("vista_presencia", fecha=fecha))

    profesores = obtener_profesores()
    presencia = obtener_presencia_dia(fecha)

    presencia_por_profesor = {}

    for p in presencia:
        pid = p["id_profesor"]
        presencia_por_profesor.setdefault(pid, []).append(p)

    presentes_ids = [
        pid for pid, eventos in presencia_por_profesor.items()
        if eventos and eventos[-1]["tipo"] == "entrada"
    ]

    return render_template(
        "vista_presencia.html",
        profesores=profesores,
        presencia_por_profesor=presencia_por_profesor,
        presentes_ids=presentes_ids,
        fecha=fecha,
        hora_real=hora_real,
        hora_lectiva=hora_lectiva,
        obtener_tramo_hora=obtener_tramo_hora,
    )

# HORARIOS
@app.route("/horarios")
def vista_horarios():
    profesores = obtener_profesores()

    fecha = request.args.get(
        "fecha",
        obtener_fecha_actual_app()
    )

    profesor_id = request.args.get("profesor_id")

    profesor_seleccionado = None
    tabla_horario = None
    fecha_inicio = None
    fecha_fin = None

    if profesor_id:
        profesor_id = int(profesor_id)

        profesor_seleccionado = next(
            (p for p in profesores if p.id_profesor == profesor_id),
            None
        )

        tabla_horario, fecha_inicio, fecha_fin = construir_tabla_horario(
            profesor_id,
            fecha
        )

    return render_template(
        "vista_horarios.html",
        profesores=profesores,
        profesor_seleccionado=profesor_seleccionado,
        tabla_horario=tabla_horario,
        dias=DIAS,
        horas=HORAS,
        fecha=fecha,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        obtener_tramo_hora=obtener_tramo_hora,
    )

if __name__ == "__main__":
    app.run(debug=True)