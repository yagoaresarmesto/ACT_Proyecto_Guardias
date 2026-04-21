from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

from modules.guardias.motor import generar_guardias, obtener_ranking_guardia
from modules.db.db_manager import obtener_guardias, asignar_guardia, sumar_guardia, obtener_profesores

app = Flask(__name__)

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

    return redirect(url_for('vista_guardias', fecha=fecha))


if __name__ == '__main__':
    app.run(debug=True)