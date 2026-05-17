import os
import time
from picamera2 import Picamera2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACES_DIR = os.path.join(BASE_DIR, "static", "faces")
OUTPUT_PATH = os.path.join(FACES_DIR, "test.jpg")


def main():
    os.makedirs(FACES_DIR, exist_ok=True)

    picam2 = Picamera2()

    config = picam2.create_still_configuration(
        main={"size": (1280, 720)}
    )

    picam2.configure(config)
    picam2.start()

    print("Cámara iniciada. Esperando enfoque...")
    time.sleep(2)

    picam2.capture_file(OUTPUT_PATH)
    picam2.stop()

    print(f"Foto guardada en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()