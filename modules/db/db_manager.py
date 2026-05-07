import sqlite3
from modules.db.models import Profesor, Guardia

DB_NAME = "ies.db"


# CONEXIÓN
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# PROFESORES
def crear_profesor(nombre, departamento=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profesores (nombre, departamento)
        VALUES (?, ?)
    """, (nombre, departamento))

    conn.commit()
    conn.close()


def obtener_profesores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profesores")
    profesores = cursor.fetchall()

    conn.close()
    return [Profesor(**p) for p in profesores]

def obtener_profesores_asignados(fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_profesor_cubre
        FROM guardias
        WHERE fecha = ? AND hora = ? AND id_profesor_cubre IS NOT NULL
    """, (fecha, hora))

    data = {row["id_profesor_cubre"] for row in cursor.fetchall()}
    conn.close()

    return data


def sumar_guardia(id_profesor):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE profesores
        SET guardias_semana = guardias_semana + 1,
            guardias_acumuladas = guardias_acumuladas + 1
        WHERE id_profesor = ?
    """, (id_profesor,))

    conn.commit()
    conn.close()

# HORARIO
def crear_horario(id_profesor, dia_semana, hora, tipo, aula=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO horario (id_profesor, dia_semana, hora, tipo, aula)
        VALUES (?, ?, ?, ?, ?)
    """, (id_profesor, dia_semana, hora, tipo, aula))

    conn.commit()
    conn.close()


def obtener_horario():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM horario")
    data = cursor.fetchall()

    conn.close()
    return data


def obtener_horario_por_dia(dia_semana):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM horario
        WHERE dia_semana = ?
    """, (dia_semana,))

    data = cursor.fetchall()
    conn.close()
    return data



# PRESENCIA
def registrar_evento(id_profesor, fecha, hora, tipo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO presencia (id_profesor, fecha, hora, tipo)
        VALUES (?, ?, ?, ?)
    """, (id_profesor, fecha, hora, tipo))

    conn.commit()
    conn.close()


def obtener_eventos(fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM presencia
        WHERE fecha = ?
        ORDER BY hora
    """, (fecha,))

    data = cursor.fetchall()
    conn.close()
    return data


def obtener_ultimo_evento(id_profesor, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM presencia
        WHERE id_profesor = ? AND fecha = ?
        ORDER BY hora DESC
        LIMIT 1
    """, (id_profesor, fecha))

    data = cursor.fetchone()
    conn.close()
    return data


def obtener_presentes(fecha):
    """
    Devuelve profesores que están actualmente dentro
    (último evento = entrada)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_profesor, tipo
        FROM presencia
        WHERE fecha = ?
        ORDER BY hora
    """, (fecha,))

    eventos = cursor.fetchall()
    conn.close()

    estado = {}

    for e in eventos:
        estado[e["id_profesor"]] = e["tipo"]

    presentes = {
        pid for pid, tipo in estado.items()
        if tipo == "entrada"
    }

    return presentes


# AUSENCIAS
def crear_ausencia(id_profesor, fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ausencias (id_profesor, fecha, hora)
        VALUES (?, ?, ?)
    """, (id_profesor, fecha, hora))

    conn.commit()
    conn.close()


def obtener_ausencias(fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM ausencias
        WHERE fecha = ?
    """, (fecha,))

    data = cursor.fetchall()
    conn.close()
    return data



# GUARDIAS
def crear_guardia(fecha, hora, aula, id_profesor_ausente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO guardias (fecha, hora, aula, id_profesor_ausente)
        VALUES (?, ?, ?, ?)
    """, (fecha, hora, aula, id_profesor_ausente))

    conn.commit()
    conn.close()


def asignar_guardia(id_guardia, id_profesor_cubre):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE guardias
        SET id_profesor_cubre = ?
        WHERE id_guardia = ?
    """, (id_profesor_cubre, id_guardia))

    conn.commit()
    conn.close()


def obtener_guardias(fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.*, 
               p1.nombre AS ausente_nombre,
               p2.nombre AS cubre_nombre
        FROM guardias g
        LEFT JOIN profesores p1 ON g.id_profesor_ausente = p1.id_profesor
        LEFT JOIN profesores p2 ON g.id_profesor_cubre = p2.id_profesor
        WHERE g.fecha = ?
        ORDER BY g.hora, g.aula
    """, (fecha,))

    data = cursor.fetchall()
    conn.close()
    return [Guardia(**g) for g in data]


def existe_guardia(fecha, hora, aula):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM guardias
        WHERE fecha = ? AND hora = ? AND aula = ?
    """, (fecha, hora, aula))

    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def obtener_horario_profesor(id_profesor):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM horario
        WHERE id_profesor = ?
        ORDER BY dia_semana, hora
    """, (id_profesor,))

    data = cursor.fetchall()
    conn.close()
    return data

def obtener_guardias_profesor_entre_fechas(id_profesor, fecha_inicio, fecha_fin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.*,
               p1.nombre AS ausente_nombre,
               p2.nombre AS cubre_nombre
        FROM guardias g
        LEFT JOIN profesores p1 ON g.id_profesor_ausente = p1.id_profesor
        LEFT JOIN profesores p2 ON g.id_profesor_cubre = p2.id_profesor
        WHERE g.id_profesor_cubre = ?
          AND g.fecha BETWEEN ? AND ?
        ORDER BY g.fecha, g.hora
    """, (id_profesor, fecha_inicio, fecha_fin))

    data = cursor.fetchall()
    conn.close()

    return [Guardia(**g) for g in data]

# LIMPIEZA
def limpiar_bd_completa():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM presencia")
    cursor.execute("DELETE FROM ausencias")
    cursor.execute("DELETE FROM guardias")
    cursor.execute("DELETE FROM horario")
    cursor.execute("DELETE FROM profesores")

    cursor.execute("DELETE FROM sqlite_sequence")

    conn.commit()
    conn.close()