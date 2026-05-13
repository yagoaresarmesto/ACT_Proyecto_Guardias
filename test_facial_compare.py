import os
import sys
import cv2


CASCADE_PATH = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"


def generar_ruta_salida(ruta_imagen):
    carpeta = os.path.dirname(ruta_imagen)
    nombre = os.path.basename(ruta_imagen)

    nombre_sin_ext, extension = os.path.splitext(nombre)

    return os.path.join(
        carpeta,
        f"{nombre_sin_ext}_detectada{extension}"
    )


def detectar_caras(ruta_imagen):
    clasificador = cv2.CascadeClassifier(CASCADE_PATH)

    if clasificador.empty():
        print("No se pudo cargar el clasificador Haar.")
        print("Ruta:", CASCADE_PATH)
        return

    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        print("No se pudo cargar la imagen.")
        return

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    caras = clasificador.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    print(f"Caras detectadas: {len(caras)}")

    if len(caras) == 0:
        print("No se detectó cara.")
        return

    print("Detección correcta.")

    for (x, y, w, h) in caras:
        cv2.rectangle(
            imagen,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    ruta_salida = generar_ruta_salida(ruta_imagen)

    cv2.imwrite(ruta_salida, imagen)

    print(f"Imagen con detección guardada en: {ruta_salida}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso:")
        print("python test_facial_compare.py ruta_imagen")
        sys.exit(1)

    detectar_caras(sys.argv[1])