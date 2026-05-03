from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime, time

from modules.guardias.motor import generar_guardias, obtener_ranking_guardia
from modules.db.db_manager import (
    obtener_guardias,
    asignar_guardia,
    sumar_guardia,
    obtener_profesores,
)

from modules.presencia.registro import obtener_presencia_dia, registrar_evento

app = Flask(__name__)


# GUARDIAS

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
        print("⚠️ No se seleccionó profesor")
        return redirect(url_for('vista_guardias', fecha=fecha))

    profesor_id = int(profesor_id)

    asignar_guardia(id_guardia, profesor_id)
    sumar_guardia(profesor_id)

    print("\n--- ASIGNACIÓN MANUAL ---")
    print("Guardia:", id_guardia)
    print("Profesor:", profesor_id)

    return redirect(url_for('vista_guardias', fecha=fecha))


# PRESENCIA

def obtener_hora_lectiva_actual():
    """
    MODO TEST
    Fuerza siempre la 3ª hora para poder probar el sistema sin depender del reloj real
    """

    return 3  # 🔥 CAMBIAR / ELIMINAR

    # DESCOMENTAR PARA REGISTRAR HORA REAL

    # ahora = datetime.now().time()
    #
    # tramos = [
    #     (time(8, 50), time(9, 40), 1),
    #     (time(9, 40), time(10, 30), 2),
    #     (time(10, 30), time(11, 20), 3),
    #
    #     (time(11, 20), time(11, 40), None),  # Recreo
    #
    #     (time(11, 40), time(12, 30), 4),
    #     (time(12, 30), time(13, 20), 5),
    #     (time(13, 20), time(14, 10), 6),
    #
    #     (time(16, 0), time(17, 0), 7),
    #     (time(17, 0), time(18, 0), 8),
    #     (time(18, 0), time(19, 0), 9),
    #     (time(19, 0), time(20, 0), 10),
    # ]
    #
    # for inicio, fin, hora in tramos:
    #     if inicio <= ahora < fin:
    #         return hora
    #
    # return None


@app.route('/presencia', methods=['GET', 'POST'])
def vista_presencia():

    fecha = request.form.get("fecha") or request.args.get("fecha") or date.today().isoformat()
    hora_real = datetime.now().strftime("%H:%M")
    hora_lectiva = obtener_hora_lectiva_actual()

    # POST → registrar entrada/salida
    if request.method == 'POST':
        profesor_id = request.form.get("profesor_id")

        if not profesor_id:
            print("⚠️ No se seleccionó profesor")
            return redirect(url_for('vista_presencia', fecha=fecha))

        hora = obtener_hora_lectiva_actual()

        print("\n--- REGISTRO DE PRESENCIA ---")
        print("Fecha:", fecha)
        print("Profesor:", profesor_id)
        print("Hora lectiva:", hora)

        registrar_evento(int(profesor_id), fecha, hora)

        return redirect(url_for('vista_presencia', fecha=fecha))

    # GET → mostrar estado
    profesores = obtener_profesores()
    presencia = obtener_presencia_dia(fecha)

    presencia_por_profesor = {}

    for p in presencia:
        if int(p["presente"]) == 1:
            presencia_por_profesor.setdefault(p["id_profesor"], []).append(int(p["hora"]))

    presentes_ids = list(presencia_por_profesor.keys())

    print("\n--- PRESENCIA ---")
    print("Hora forzada:", hora_lectiva)
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