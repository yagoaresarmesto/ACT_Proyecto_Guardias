from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

from modules.guardias.motor import generar_guardias, obtener_ranking_guardia
from modules.db.db_manager import (
    obtener_guardias,
    asignar_guardia,
    sumar_guardia,
    obtener_profesores,
    borrar_presencia_hora
)

from modules.presencia.registro import registrar, obtener_presencia_dia

app = Flask(__name__)

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

    print("\nGUARDIAS")
    print("Fecha:", fecha)

    for g in guardias:
        print(f"Aula {g.aula} - Hora {g.hora}")
        print("Ausente:", g.ausente_nombre)
        print("Ranking:", ranking_por_guardia[g.id_guardia])

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

    print("\n--- ASIGNACIÓN MANUAL ---")
    print("Guardia:", id_guardia)
    print("Profesor asignado:", profesor_id)

    return redirect(url_for('vista_guardias', fecha=fecha))


# PRESENCIA
@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():

    fecha = request.form.get("fecha") or request.args.get("fecha") or date.today().isoformat()
    hora = int(request.form.get("hora") or request.args.get("hora") or 1)

    if request.method == 'POST':
        seleccionados = request.form.getlist("profesores")

        print("\n--- GUARDANDO PRESENCIA ---")
        print("Fecha:", fecha)
        print("Hora:", hora)
        print("Seleccionados:", seleccionados)

        # 🔥 BORRAR presencia anterior
        borrar_presencia_hora(fecha, hora)

        # 🔥 INSERTAR nueva presencia
        for p_id in seleccionados:
            registrar(int(p_id), fecha, hora)

        return redirect(url_for('vista_presencia', fecha=fecha, hora=hora))

    # Obtener datos
    profesores = obtener_profesores()
    presencia = obtener_presencia_dia(fecha)

    # 🔥 FILTRAR presentes por hora
    presentes = {
        p["id_profesor"]
        for p in presencia
        if int(p["hora"]) == int(hora) and int(p["presente"]) == 1
    }

    print("\n--- PRESENCIA ACTUAL ---")
    print("Fecha:", fecha)
    print("Hora:", hora)
    print("Presentes:", presentes)

    return render_template(
        "vista_presencia.html",
        profesores=profesores,
        presencia=presencia,
        presentes=presentes,
        fecha=fecha,
        hora=hora
    )


if __name__ == '__main__':
    app.run(debug=True)