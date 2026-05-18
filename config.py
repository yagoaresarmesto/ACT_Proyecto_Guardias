import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la base de datos SQLite
DB_PATH = os.path.join(BASE_DIR, "ies.db")

# Configuración de presencia (modo test)
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1 # Hora en formato 10h [1-10]

METODO_PRESENCIA = os.getenv("METODO_PRESENCIA", "facial")

#Configuración para reconocimiento facial
FACES_DIR = os.path.join(BASE_DIR, "static", "faces")

NUM_REFERENCIAS_FACIALES = 7
MAX_INTENTOS_REFERENCIA = 20
TOLERANCIA_RECONOCIMIENTO = 0.5 #Estable 
TIEMPO_VERIFICACION_FACIAL = 15