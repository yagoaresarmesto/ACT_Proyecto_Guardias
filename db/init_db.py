import sqlite3
import os

def init_db():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "ies.db")
    schema_path = os.path.join(BASE_DIR, "db", "schema.sql")

    #eliminar BD anterior en pruebas
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Base anterior eliminada.")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Base de datos creada en:", db_path)
    except Exception as e:
        print("Error al crear la base de datos:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
