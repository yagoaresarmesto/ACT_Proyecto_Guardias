import os
import time
from datetime import datetime

from picamera2 import Picamera2, Preview


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

FACES_DIR = os.path.join(BASE_DIR, "static", "faces")


def asegurar_carpeta_faces():
    os.makedirs(FACES_DIR, exist_ok=True)


def capturar_foto(ruta_destino):
    asegurar_carpeta_faces()

    picam2 = Picamera2()

    try:
        config = picam2.create_preview_configuration(
            main={"size": (1280, 720)}
        )

        picam2.configure(config)

        picam2.start_preview(Preview.QTGL)
        picam2.start()

        print("Preview abierta.")
        print("Colócate bien frente a la cámara.")
        input("Pulsa ENTER para capturar la foto...")

        picam2.capture_file(ruta_destino)

        print(f"Foto guardada en: {ruta_destino}")
        return ruta_destino

    finally:
        picam2.stop_preview()
        picam2.stop()
        picam2.close()
        time.sleep(1)


def ruta_referencia_profesor(id_profesor):
    asegurar_carpeta_faces()
    return os.path.join(FACES_DIR, f"profesor_{id_profesor}_ref.jpg")


def ruta_verificacion_profesor(id_profesor):
    asegurar_carpeta_faces()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"profesor_{id_profesor}_check_{timestamp}.jpg"

    return os.path.join(FACES_DIR, nombre)


def capturar_referencia_profesor(id_profesor):
    ruta = ruta_referencia_profesor(id_profesor)
    return capturar_foto(ruta)


def capturar_verificacion_profesor(id_profesor):
    ruta = ruta_verificacion_profesor(id_profesor)
    return capturar_foto(ruta)