import os
import sys
import time
import pickle
import cv2

import face_recognition

from picamera2 import Picamera2, Preview


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FACES_DIR = os.path.join(
    BASE_DIR,
    "static",
    "faces",
    "test_live"
)

ENCODINGS_PATH = os.path.join(
    FACES_DIR,
    "encodings.pkl"
)


def asegurar_directorio():
    os.makedirs(FACES_DIR, exist_ok=True)


def iniciar_camara():
    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (1280, 720)}
    )

    picam2.configure(config)

    picam2.start_preview(Preview.QTGL)
    picam2.start()

    return picam2


def registrar_referencias():
    asegurar_directorio()

    picam2 = iniciar_camara()

    encodings_guardados = []

    print("Registro facial iniciado.")
    print("Mira a cámara y cambia un poco el ángulo.")
    print("Capturando 5 referencias...")

    try:
        for i in range(5):
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(frame)

            if encodings:
                encodings_guardados.append(encodings[0])

                print(f"Referencia {i+1}/5 guardada")
            else:
                print(f"No se detectó cara en captura {i+1}")

            time.sleep(1)

        with open(ENCODINGS_PATH, "wb") as f:
            pickle.dump(encodings_guardados, f)

        print("Referencias guardadas en:")
        print(ENCODINGS_PATH)

    finally:
        picam2.stop_preview()
        picam2.stop()
        picam2.close()


def verificar_en_vivo():
    if not os.path.exists(ENCODINGS_PATH):
        print("No existen referencias guardadas.")
        return

    with open(ENCODINGS_PATH, "rb") as f:
        referencias = pickle.load(f)

    picam2 = iniciar_camara()

    print("Verificación facial iniciada...")
    print("Tienes 10 segundos para colocarte.")

    inicio = time.time()

    try:
        while time.time() - inicio < 10:
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(frame)

            if not encodings:
                print("No se detectó cara")
                continue

            encoding_actual = encodings[0]

            resultados = face_recognition.compare_faces(
                referencias,
                encoding_actual,
                tolerance=0.5
            )

            if True in resultados:
                print("RECONOCIDO")
                return

            print("Cara no reconocida")

            time.sleep(0.5)

        print("Tiempo agotado.")

    finally:
        picam2.stop_preview()
        picam2.stop()
        picam2.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso:")
        print("python test_live_face_reference.py registrar")
        print("python test_live_face_reference.py verificar")
        sys.exit(1)

    modo = sys.argv[1]

    if modo == "registrar":
        registrar_referencias()

    elif modo == "verificar":
        verificar_en_vivo()

    else:
        print("Modo no válido.")