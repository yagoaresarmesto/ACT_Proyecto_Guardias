import sqlite3

DB_PATH = "ies.db"

#Abre conexión con la base de datos
def get_connection():
    return sqlite3.connect(DB_PATH)

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