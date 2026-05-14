import sys
import cv2
import numpy as np


CASCADE_PATH = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
UMBRAL = 20

def detectar_y_recortar_cara(ruta_imagen):
    clasificador = cv2.CascadeClassifier(CASCADE_PATH)

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        print(f"No se pudo cargar: {ruta_imagen}")
        return None

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    caras = clasificador.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(caras) == 0:
        print(f"No se detectó cara en: {ruta_imagen}")
        return None

    # Usamos la primera cara detectada
    x, y, w, h = caras[0]

    cara = gris[y:y+h, x:x+w]

    # Normalizamos tamaño
    cara = cv2.resize(cara, (200, 200))

    return cara


def comparar_caras(ruta_ref, ruta_check):
    cara_ref = detectar_y_recortar_cara(ruta_ref)
    cara_check = detectar_y_recortar_cara(ruta_check)

    if cara_ref is None or cara_check is None:
        print("No se pudo comparar.")
        return

    # Diferencia absoluta entre imágenes
    diferencia = cv2.absdiff(cara_ref, cara_check)

    # Media de diferencia
    score = np.mean(diferencia)

    print(f"Score de diferencia: {score:.2f}")

    # Cuanto más bajo, más parecidas
    if score < UMBRAL:
        print("RESULTADO: Probablemente la misma persona")
    else:
        print("RESULTADO: Personas diferentes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso:")
        print("python test_facial_compare.py ref.jpg check.jpg")
        sys.exit(1)

    comparar_caras(sys.argv[1], sys.argv[2])