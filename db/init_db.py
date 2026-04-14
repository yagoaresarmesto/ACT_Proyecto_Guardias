import sqlite3
import os

def init_db():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    db_path = os.path.join(BASE_DIR, "ies.db")
    schema_path = os.path.join(BASE_DIR, "db", "schema.sql")

    conn = sqlite3.connect(db_path)

    with open(schema_path, "r") as f:
        conn.executescript(f.read())

    conn.close()
    print("Base de datos creada correctamente en:", db_path)


if __name__ == "__main__":
    init_db()