import sqlite3
import os
import sys

MODULES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(MODULES_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import DB_PATH


def init_db():
    schema_path = os.path.join(
        MODULES_DIR,
        "db",
        "schema.sql"
    )

    print("schema_path:", schema_path)
    print("db_path:", DB_PATH)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Base anterior eliminada.")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        print("Base de datos creada en:", DB_PATH)

    except Exception as e:
        print("Error al crear la base de datos:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()