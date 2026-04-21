import sqlite3
DB_NAME = "ies.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


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
    return profesores


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



def registrar_presencia(id_profesor, fecha, hora, presente=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO presencia (id_profesor, fecha, hora, presente)
        VALUES (?, ?, ?, ?)
    """, (id_profesor, fecha, hora, presente))

    conn.commit()
    conn.close()


def obtener_presencia(fecha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM presencia
        WHERE fecha = ?
    """, (fecha,))

    data = cursor.fetchall()
    conn.close()
    return data


def obtener_presentes(fecha, hora):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_profesor FROM presencia
        WHERE fecha = ? AND hora = ? AND presente = 1
    """, (fecha, hora))

    data = {row["id_profesor"] for row in cursor.fetchall()}
    conn.close()
    return data



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
    return data

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