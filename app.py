from flask import Flask, render_template, request
from datetime import date

from modules.guardias.motor import generar_guardias
from modules.db.db_manager import obtener_guardias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardias')
def vista_guardias():
    # 1. Fecha seleccionada o hoy
    fecha = request.args.get("fecha", date.today().isoformat())

    # 2. Día semana (simplificado)
    dia_semana = 1  # luego lo haremos dinámico

    # 3. Generar guardias (motor)
    generar_guardias(dia_semana, fecha)

    # 4. Obtener guardias de BD
    guardias = obtener_guardias(fecha)

    # 5. Renderizar
    return render_template(
        "vista_guardias.html",
        guardias=guardias,
        fecha=fecha
    )

if __name__ == '__main__':
    app.run(debug=True)