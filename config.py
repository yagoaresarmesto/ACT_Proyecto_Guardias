import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "ies.db")

MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1

METODO_PRESENCIA = os.getenv("METODO_PRESENCIA", "manual")