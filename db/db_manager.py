import sqlite3
from wsgiref.util import request_uri

DB_PATH = "ies.db"

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