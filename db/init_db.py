import sqlite3
#Crea la base de datos de sqlLite

def init_db():
    conn = sqlite3.connect("ies.db")

    with open("db/schema.sql", "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.close()
    print("Base de datos creada")


if __name__ == "__main__":
    init_db()