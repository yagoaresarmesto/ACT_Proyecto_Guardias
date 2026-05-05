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
from modules.utils.tiempo import obtener_hora_lectiva_actual

app = Flask(__name__)

#MODO TEST
MODO_TEST = True
HORA_TEST = 6


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



# GUARDIAS
@app.route('/guardias')
def vista_guardias():
    fecha = request.args.get("fecha", date.today().isoformat())
    hora_real = datetime.now().strftime("%H:%M")
    dia_semana = datetime.fromisoformat(fecha).isoweekday()

    # 🔥 HORA ACTUAL
    if MODO_TEST:
        hora_actual = HORA_TEST
    else:
        hora_actual = obtener_hora_lectiva_actual()

    generar_guardias(dia_semana, fecha)
    guardias = obtener_guardias(fecha)

    ranking_por_guardia = {}

    for g in guardias:
        ranking_por_guardia[g.id_guardia] = obtener_ranking_guardia(
            dia_semana,
            fecha,
            g.hora
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
        fecha_actual=date.today().isoformat(),
        hora_real = hora_real
    )


@app.route('/asignar_guardia', methods=['POST'])
def asignar_guardia_manual():
    id_guardia = int(request.form['id_guardia'])
    profesor_id = request.form.get('profesor_id')
    fecha = request.form.get('fecha')

    if not profesor_id:
        return redirect(url_for('vista_guardias', fecha=fecha))

    profesor_id = int(profesor_id)

    asignar_guardia(id_guardia, profesor_id)
    sumar_guardia(profesor_id)

    return redirect(url_for('vista_guardias', fecha=fecha))


# PRESENCIA

@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():

    fecha = request.form.get("fecha") or request.args.get("fecha") or date.today().isoformat()
    hora_real = datetime.now().strftime("%H:%M")

    if MODO_TEST:
        hora_lectiva = HORA_TEST
    else:
        hora_lectiva = obtener_hora_lectiva_actual()

    if request.method == 'POST':
        profesor_id = request.form.get("profesor_id")

        if not profesor_id:
            return redirect(url_for('vista_presencia', fecha=fecha))

        if not hora_lectiva:
            return redirect(url_for('vista_presencia', fecha=fecha))

        registrar_evento(int(profesor_id), fecha, hora_lectiva)

        return redirect(url_for('vista_presencia', fecha=fecha))

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
        obtener_tramo_hora=obtener_tramo_hora
    )


if __name__ == '__main__':
    app.run(debug=True)