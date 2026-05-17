import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la base de datos SQLite
DB_PATH = os.path.join(BASE_DIR, "ies.db")

# Configuración de presencia
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 10 # Hora en formato 10h [1-10]

METODO_PRESENCIA = os.getenv("METODO_PRESENCIA", "facial")

#Configuración para reconocimiento facial
FACES_DIR = os.path.join(BASE_DIR, "static", "faces")

NUM_REFERENCIAS_FACIALES = 5
MAX_INTENTOS_REFERENCIA = 15
TOLERANCIA_RECONOCIMIENTO = 0.5
TIEMPO_VERIFICACION_FACIAL = 10