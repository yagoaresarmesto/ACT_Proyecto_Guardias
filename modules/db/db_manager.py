import sqlite3
import os
from . import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "ies.db")


def get_connection():
    """Abre conexión con SQLite y activa claves foráneas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def insertar_profesor(nombre, departamento, rfid_uid=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO profesores(nombre, departamento, rfid_uid) VALUES (?, ?, ?);",
        (nombre, departamento, rfid_uid),
    )
    conn.commit()
    conn.close()


def get_all_profesores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profesores ORDER BY nombre;")
    rows = cur.fetchall()
    conn.close()
    return [models.Profesor(**dict(row)) for row in rows]


def obtener_profesor_por_id(id_profesor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profesores WHERE id_profesor = ?", (id_profesor,))
    row = cur.fetchone()
    conn.close()
    return models.Profesor(**dict(row)) if row else None


def insertar_horario(id_profesor, dia_semana, hora, aula, tipo="clase"):
    """Crea un registro de horario."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO horario(id_profesor, dia_semana, hora, tipo, aula) VALUES (?, ?, ?, ?, ?)",
        (id_profesor, dia_semana, hora, tipo, aula),
    )
    conn.commit()
    conn.close()


def get_all_horarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM horario;")
    rows = cur.fetchall()
    conn.close()
    return [models.Horario(**dict(row)) for row in rows]


# Alias de compatibilidad
def obtener_horarios():
    return get_all_horarios()


def registrar_presencia(id_profesor, fecha, hora, presente):
    """Registra la presencia del profesor."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO presencia(id_profesor, fecha, hora, presente) VALUES (?, ?, ?, ?);",
        (id_profesor, fecha, hora, int(presente)),
    )
    conn.commit()
    conn.close()


def get_all_presencias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM presencia;")
    rows = cur.fetchall()
    conn.close()
    return [models.Presencia(**dict(row)) for row in rows]


# Alias de compatibilidad
def obtener_presencia():
    return get_all_presencias()


def get_ausentes(dia_semana, fecha):
    """Versión provisional: profesores sin registro de presencia en la fecha dada."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_profesor, p.nombre
        FROM profesores p
        WHERE p.id_profesor NOT IN (
            SELECT id_profesor FROM presencia WHERE fecha = ?
        )
        ORDER BY p.nombre;
    """, (fecha,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Alias de compatibilidad
def obtener_ausentes(dia_semana, fecha):
    return get_ausentes(dia_semana, fecha)


def guardar_guardia(aula, id_profesor_ausente, fecha, hora, id_profesor_cubre=None):
    """Inserta una guardia manualmente."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO guardias(fecha, hora, aula, id_profesor_ausente, id_profesor_cubre)
           VALUES (?, ?, ?, ?, ?);""",
        (fecha, hora, aula, id_profesor_ausente, id_profesor_cubre),
    )
    conn.commit()
    conn.close()


def obtener_guardia():
    """Devuelve todas las guardias registradas."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM guardias;")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def limpiar_bd_completa():
    """Elimina todos los registros de todas las tablas."""
    conn = get_connection()
    cur = conn.cursor()
    tablas = ["presencia", "ausencias", "guardias", "horario", "profesores"]
    for t in tablas:
        cur.execute(f"DELETE FROM {t};")
    conn.commit()
    conn.close()
    print("🧹 Base de datos limpiada correctamente.")

