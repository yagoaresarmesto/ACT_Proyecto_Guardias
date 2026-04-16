import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ies.db")

#Abre conexión con la base de datos
def get_connection():
    return sqlite3.connect(DB_PATH)

#Profesores
#Crear profesor (test)
def crear_profesor(nombre):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO profesores (nombre) VALUES (?)",
        (nombre,)
    )
    conn.commit()
    conn.close()

#Obtener profesores (test)
def obtener_profesores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profesores")
    profesores = cursor.fetchall()

    conn.close()
    return profesores

def obtener_profesor_por_id(profesor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM profesores WHERE id = ?",
        (profesor_id,)
    )

    profesor = cursor.fetchone()

    conn.close()
    return profesor

#Horarios

#Crear horario (test)
def crear_horario(profesor_id, dia, hora, aula):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO horarios (profesor_id, dia, hora, aula) VALUES (?, ?, ?, ?)",
        (profesor_id, dia, hora, aula)
    )

    conn.commit()
    conn.close()

#Obtener horarios (test)
def obtener_horarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM horarios")
    horarios = cursor.fetchall()

    conn.close()
    return horarios

#Entrada

def registrar_entrada(profesor_id, fecha, hora_entrada):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO presencia (profesor_id, fecha, hora_entrada) VALUES (?, ?, ?)",
        (profesor_id, fecha, hora_entrada)
    )
    print("Registrando entrada:", profesor_id)
    conn.commit()
    conn.close()

#Ver presencia

def obtener_presencia():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM presencia")
    datos = cursor.fetchall()

    conn.close()
    return datos


#Obtener ausentes

def obtener_ausentes(dia, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    # Profesores que deberían estar ese día
    cursor.execute(
        "SELECT DISTINCT profesor_id FROM horarios WHERE dia = ?",
        (dia,)
    )
    profesores_horario = {row[0] for row in cursor.fetchall()}

    # Profesores que han fichado ese día
    cursor.execute(
        "SELECT DISTINCT profesor_id FROM presencia WHERE fecha = ?",
        (fecha,)
    )
    profesores_presentes = {row[0] for row in cursor.fetchall()}

    conn.close()

    # Diferencia
    ausentes = profesores_horario - profesores_presentes

    return ausentes

def obtener_guardia(aula, hora, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT profesor_id FROM guardias
        WHERE aula = ? AND hora = ? AND fecha = ?
    """, (aula, hora, fecha))

    resultado = cursor.fetchone()

    conn.close()

    return resultado[0] if resultado else None

def sumar_guardia(profesor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE profesores
        SET guardias_acumuladas = guardias_acumuladas + 1,
            guardias_semana = guardias_semana + 1
        WHERE id = ?
    """, (profesor_id,))

    conn.commit()
    conn.close()

def guardar_guardia(aula, hora, fecha, profesor_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO guardias (profesor_id, aula, hora, fecha)
        VALUES (?, ?, ?, ?)
    """, (profesor_id, aula, hora, fecha))

    conn.commit()
    conn.close()


#Borrar base de datos
def limpiar_bd_completa():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM guardias")   # 🔥 FALTABA
    cursor.execute("DELETE FROM presencia")
    cursor.execute("DELETE FROM horarios")
    cursor.execute("DELETE FROM profesores")

    cursor.execute("DELETE FROM sqlite_sequence")

    conn.commit()
    conn.close()