from flask import Flask, render_template
from modules.guardias.motor import asignar_guardias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardias')
def vista_guardias():

    guardias = asignar_guardias("Lunes", "2026-04-09")
    return render_template('vista_guardias.html', guardias=guardias)

@app.route('/presencia')
def vista_presencia():
    return render_template('vista_presencia.html')

if __name__ == '__main__':
    app.run(debug=True)