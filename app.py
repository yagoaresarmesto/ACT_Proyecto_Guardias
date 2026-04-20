from flask import Flask, render_template, redirect, url_for, request
from modules.guardias.motor import obtener_guardias_para_vista
from modules.db.db_manager import sumar_guardia, guardar_guardia, obtener_profesores, registrar_entrada, obtener_presencia
from datetime import date


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardias')
def vista_guardias():
    fecha = request.args.get("fecha", date.today().isoformat())
    guardias = obtener_guardias_para_vista("Lunes", fecha)

    return render_template(
        "vista_guardias.html",
        guardias=guardias,
        fecha=fecha
    )
@app.route('/asignar_guardia', methods=['POST'])
def asignar_guardia():
    hoy = date.today().isoformat()
    profesor_id = request.form['profesor_id']
    aula = request.form['aula']
    hora = int(request.form['hora'])

    if not profesor_id:
        return redirect(url_for('vista_guardias'))

    profesor_id = int(profesor_id)

    guardar_guardia(aula, hora, hoy, profesor_id)
    sumar_guardia(profesor_id)

    return redirect(url_for('vista_guardias'))



@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():
    fecha = request.args.get("fecha", date.today().isoformat())
    if request.method == 'POST':
        profesor_id = request.form['profesor_id']
        registrar_entrada(profesor_id, fecha, "8:00")

        return redirect(url_for('vista_presencia', fecha = fecha))

    profesores = obtener_profesores()
    presencia = obtener_presencia()

    presentes = {p[1] for p in presencia if p[2] == fecha}

    return render_template(
        'vista_presencia.html',
        profesores=profesores,
        presentes=presentes,
        fecha = fecha
    )
if __name__ == '__main__':
    app.run(debug=True)