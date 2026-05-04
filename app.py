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

app = Flask(__name__)

# -----------------------------
# 🔥 TRAMOS HORARIOS (ÚNICA FUENTE)
# -----------------------------
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
    if tramo:
        return f"{tramo[0]} - {tramo[1]}"
    return ""

# -----------------------------
# GUARDIAS
# -----------------------------
@app.route('/guardias')
def vista_guardias():
    fecha = request.args.get("fecha", date.today().isoformat())
    dia_semana = datetime.fromisoformat(fecha).isoweekday()

    generar_guardias(dia_semana, fecha)
    guardias = obtener_guardias(fecha)

    ranking_por_guardia = {}

    for g in guardias:
        ranking_por_guardia[g.id_guardia] = obtener_ranking_guardia(
            dia_semana,
            fecha,
            g.hora
        )

    print("\n--- GUARDIAS ---")
    print("Fecha:", fecha)

    for g in guardias:
        print(f"Aula {g.aula} - Hora {g.hora}")
        print("Ausente:", g.ausente_nombre)

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
        obtener_tramo_hora=obtener_tramo_hora
    )


@app.route('/asignar_guardia', methods=['POST'])
def asignar_guardia_manual():

    id_guardia = int(request.form['id_guardia'])
    profesor_id = request.form.get('profesor_id')
    fecha = request.form.get('fecha')

    if not profesor_id:
        print("⚠️ No se seleccionó profesor")
        return redirect(url_for('vista_guardias', fecha=fecha))

    profesor_id = int(profesor_id)

    asignar_guardia(id_guardia, profesor_id)
    sumar_guardia(profesor_id)

    print("\n--- ASIGNACIÓN MANUAL ---")
    print("Guardia:", id_guardia)
    print("Profesor:", profesor_id)

    return redirect(url_for('vista_guardias', fecha=fecha))


# -----------------------------
# PRESENCIA
# -----------------------------
def obtener_hora_lectiva_actual():
    """
    MODO TEST
    """
    return 3

    # -----------------------------
    # DESCOMENTAR
    # -----------------------------
    # ahora = datetime.now().time()
    #
    # for hora, (inicio_str, fin_str) in TRAMOS_HORARIOS.items():
    #     inicio = datetime.strptime(inicio_str, "%H:%M").time()
    #     fin = datetime.strptime(fin_str, "%H:%M").time()
    #
    #     if inicio <= ahora < fin:
    #         return hora
    #
    # return None


@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():

    fecha = request.form.get("fecha") or request.args.get("fecha") or date.today().isoformat()
    hora_real = datetime.now().strftime("%H:%M")
    hora_lectiva = obtener_hora_lectiva_actual()

    # 🔹 POST → registrar entrada/salida
    if request.method == 'POST':
        profesor_id = request.form.get("profesor_id")

        if not profesor_id:
            print("⚠️ No se seleccionó profesor")
            return redirect(url_for('vista_presencia', fecha=fecha))

        print("\n--- REGISTRO DE PRESENCIA ---")
        print("Fecha:", fecha)
        print("Profesor:", profesor_id)
        print("Hora lectiva:", hora_lectiva)

        registrar_evento(int(profesor_id), fecha, hora_lectiva)

        return redirect(url_for('vista_presencia', fecha=fecha))

    profesores = obtener_profesores()
    presencia = obtener_presencia_dia(fecha)

    presencia_por_profesor = {}

    for p in presencia:
        if int(p["presente"]) == 1:
            presencia_por_profesor.setdefault(
                p["id_profesor"], []
            ).append(int(p["hora"]))

    presentes_ids = list(presencia_por_profesor.keys())

    print("\n--- PRESENCIA ---")
    print("Hora actual:", hora_lectiva)
    print("Presentes:", presentes_ids)

    return render_template(
        "vista_presencia.html",
        profesores=profesores,
        presencia_por_profesor=presencia_por_profesor,
        presentes_ids=presentes_ids,
        fecha=fecha,
        hora_real=hora_real,
        hora_lectiva=hora_lectiva
    )


if __name__ == '__main__':
    app.run(debug=True)