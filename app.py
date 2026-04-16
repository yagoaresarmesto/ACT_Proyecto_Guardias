from flask import Flask, render_template, redirect, url_for, request
from modules.guardias.motor import asignar_guardias, obtener_guardias_para_vista
from db.db_manager import sumar_guardia, guardar_guardia, obtener_profesores, registrar_entrada, obtener_presencia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardias')
def vista_guardias():
    guardias = obtener_guardias_para_vista("Lunes", "2026-04-09")
    return render_template("vista_guardias.html", guardias=guardias)

@app.route('/asignar_guardia', methods=['POST'])
def asignar_guardia():
    profesor_id = request.form['profesor_id']
    aula = request.form['aula']
    hora = int(request.form['hora'])

    if not profesor_id:
        return redirect(url_for('vista_guardias'))

    profesor_id = int(profesor_id)

    guardar_guardia(aula, hora, "2026-04-09", profesor_id)
    sumar_guardia(profesor_id)

    return redirect(url_for('vista_guardias'))



@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():
    if request.method == 'POST':
        profesor_id = request.form['profesor_id']
        registrar_entrada(profesor_id, "2026-04-09", "08:00")

        return redirect(url_for('vista_presencia'))

    profesores = obtener_profesores()
    presencia = obtener_presencia()

    presentes = {p[1] for p in presencia if p[2] == "2026-04-09"}

    return render_template(
        'vista_presencia.html',
        profesores=profesores,
        presentes=presentes
    )
if __name__ == '__main__':
    app.run(debug=True)