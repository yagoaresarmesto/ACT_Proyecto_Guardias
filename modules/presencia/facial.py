import os
import time
import pickle

import cv2
import face_recognition

from picamera2 import Picamera2, Preview

from config import (
    FACES_DIR,
    NUM_REFERENCIAS_FACIALES,
    MAX_INTENTOS_REFERENCIA,
    TOLERANCIA_RECONOCIMIENTO,
    TIEMPO_VERIFICACION_FACIAL,
)


def asegurar_carpeta_faces():
    os.makedirs(FACES_DIR, exist_ok=True)


def carpeta_profesor(id_profesor):
    asegurar_carpeta_faces()

    ruta = os.path.join(
        FACES_DIR,
        f"profesor_{id_profesor}"
    )

    os.makedirs(ruta, exist_ok=True)

    return ruta


def ruta_encodings_profesor(id_profesor):
    return os.path.join(
        carpeta_profesor(id_profesor),
        "encodings.pkl"
    )


def iniciar_camara():
    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (1280, 720)}
    )

    picam2.configure(config)

    picam2.start_preview(Preview.QTGL)
    picam2.start()

    return picam2


def cerrar_camara(picam2):
    try:
        picam2.stop_preview()
    except Exception:
        pass

    try:
        picam2.stop()
    except Exception:
        pass

    try:
        picam2.close()
    except Exception:
        pass

    time.sleep(1)


def preparar_frame_para_face_recognition(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def registrar_referencias_profesor(id_profesor):
    ruta_pkl = ruta_encodings_profesor(id_profesor)

    picam2 = iniciar_camara()

    encodings_guardados = []
    intentos = 0

    print("Registro facial iniciado.")
    print("Mira a cámara y cambia ligeramente el ángulo.")
    print(
        f"Objetivo: capturar "
        f"{NUM_REFERENCIAS_FACIALES} referencias válidas."
    )
    print(f"Intentos máximos: {MAX_INTENTOS_REFERENCIA}")

    try:
        while (
            len(encodings_guardados) < NUM_REFERENCIAS_FACIALES
            and intentos < MAX_INTENTOS_REFERENCIA
        ):
            intentos += 1
            time.sleep(1)

            frame = picam2.capture_array()
            frame_rgb = preparar_frame_para_face_recognition(frame)

            encodings = face_recognition.face_encodings(frame_rgb)

            if encodings:
                encodings_guardados.append(encodings[0])
                print(
                    f"Referencia {len(encodings_guardados)}/"
                    f"{NUM_REFERENCIAS_FACIALES} guardada"
                )
            else:
                print(
                    f"No se detectó cara en intento "
                    f"{intentos}/{MAX_INTENTOS_REFERENCIA}"
                )

        if len(encodings_guardados) < NUM_REFERENCIAS_FACIALES:
            print(
                f"Registro incompleto: solo se consiguieron "
                f"{len(encodings_guardados)}/"
                f"{NUM_REFERENCIAS_FACIALES} referencias."
            )

        if not encodings_guardados:
            print("No se pudo registrar ninguna referencia facial.")
            return None

        with open(ruta_pkl, "wb") as f:
            pickle.dump(encodings_guardados, f)

        print("Referencias faciales guardadas en:")
        print(ruta_pkl)

        return ruta_pkl

    finally:
        cerrar_camara(picam2)


def cargar_referencias(ruta_encodings):
    if not os.path.exists(ruta_encodings):
        print("No existe archivo de referencias:", ruta_encodings)
        return []

    with open(ruta_encodings, "rb") as f:
        return pickle.load(f)


def verificar_profesor_en_vivo(
    ruta_encodings,
    tolerancia=TOLERANCIA_RECONOCIMIENTO
):
    referencias = cargar_referencias(ruta_encodings)

    if not referencias:
        print("No hay referencias faciales cargadas.")
        return False

    picam2 = iniciar_camara()

    print("Verificación facial iniciada.")
    print(
        f"Tienes {TIEMPO_VERIFICACION_FACIAL} "
        f"segundos para colocarte."
    )

    inicio = time.time()

    try:
        while time.time() - inicio < TIEMPO_VERIFICACION_FACIAL:
            frame = picam2.capture_array()
            frame_rgb = preparar_frame_para_face_recognition(frame)

            encodings_actuales = face_recognition.face_encodings(frame_rgb)

            if not encodings_actuales:
                print("No se detectó cara.")
                time.sleep(0.5)
                continue

            encoding_actual = encodings_actuales[0]

            distancias = face_recognition.face_distance(
                referencias,
                encoding_actual
            )

            distancia_minima = min(distancias)

            resultados = face_recognition.compare_faces(
                referencias,
                encoding_actual,
                tolerance=tolerancia
            )

            print(f"Distancia mínima: {distancia_minima:.4f}")

            if True in resultados:
                print("Profesor reconocido.")
                return True

            print("Cara detectada, pero no coincide.")
            time.sleep(0.5)

        print("Tiempo de verificación agotado.")
        return False

    finally:
        cerrar_camara(picam2)