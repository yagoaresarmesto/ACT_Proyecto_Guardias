# Raspberry Pi Camera y reconocimiento facial

## Paquetes del sistema

### Cámara Raspberry Pi

Instalación:

sudo apt install -y python3-picamera2

Importante:
- picamera2 debe instalarse por apt, no por pip.
- Para usar picamera2 dentro del entorno virtual, el .venv debe crearse con --system-site-packages.

---

### OpenCV

Instalación:

sudo apt install -y python3-opencv

Importante:
- OpenCV instalado por apt funciona mejor en Raspberry Pi que instalarlo por pip.

---

### face_recognition

Dependencias del sistema:

sudo apt install -y cmake build-essential python3-dev

Instalación dentro del entorno virtual:

pip install face_recognition

Importante:
- face_recognition compila dlib durante la instalación.
- La instalación puede tardar bastante tiempo.
- En Raspberry Pi con poca RAM puede ser necesario aumentar la swap.
- En Raspberry Pi 5 con 8 GB funciona correctamente. Pero si tiene 4GB de RAM probablemente se te congele en la instalacion, asi que que toca hacer swap
- Para hacer swap he seguido este video: https://www.youtube.com/watch?v=XNSSbSJ4lB4&list=PLywraUhcWmsCgxBEOPQWx6BWZhq4CxHh8&index=3
---

## Entorno virtual

Crear entorno virtual:

python3 -m venv --system-site-packages .venv

Activar entorno:

source .venv/bin/activate

Importante:
- --system-site-packages es necesario para que el .venv pueda acceder a picamera2 y OpenCV instalados por apt.

---

## Comprobaciones rápidas

### Detectar cámaras disponibles

rpicam-hello --list-cameras

### Foto rápida con preview de 5 segundos

rpicam-still -t 5000 -o foto_prueba.jpg

### Probar captura desde Python

python test_facial_capture.py

### Probar registro y verificación facial

Registrar referencias:

python test_live_face_reference.py registrar

Verificar identidad:

python test_live_face_reference.py verificar

---

## Conversión de imágenes

### Instalar ImageMagick

sudo apt install -y imagemagick

### Convertir imagen a JPG

convert imagen_origen.png imagen_convertida.jpg

---

## Advertencias habituales

### QStandardPaths warning

Puede aparecer este mensaje:

QStandardPaths: wrong permissions on runtime directory...

Importante:
- No impide que la cámara funcione.
- Puede ignorarse si todo funciona correctamente.