# Raspberry Pi Camera y reconocimiento facial

## Paquetes del sistema

### C�mara Raspberry Pi

Instalaci�n:

```bash
sudo apt install -y python3-picamera2
```

Importante:
- `picamera2` es mejor instalarlo por `apt`, no por `pip`.
- Para usar `picamera2` dentro del entorno virtual, el `.venv` debe crearse con `--system-site-packages`, para poder acceder a paquetes instalados fuera del entorno virtual.

---

### OpenCV

Instalaci�n:

```bash
sudo apt install -y python3-opencv
```

Importante:
- OpenCV instalado por `apt` funciona mejor en Raspberry Pi que instalarlo por `pip`.

---

### face_recognition

Dependencias del sistema:

```bash
sudo apt install -y cmake build-essential python3-dev
```

Instalaci�n dentro del entorno virtual:

```bash
pip install face_recognition
```

Importante:
- `face_recognition` compila `dlib` durante la instalaci�n.
- La instalaci�n puede tardar bastante tiempo.
- En Raspberry Pi con poca RAM puede ser necesario aumentar la swap.
- En Raspberry Pi 5 con 8 GB funciona correctamente.
- En Raspberry Pi con 4 GB de RAM la instalaci�n puede congelar el sistema durante la compilaci�n.

Si la Raspberry Pi se congela durante la instalaci�n, crear swap adicional temporal:

Crear swap de 4 GB:

```bash
sudo fallocate -l 4G /var/swap
sudo chmod 600 /var/swap
sudo mkswap /var/swap
sudo swapon /var/swap
```

Comprobar swap:

```bash
swapon --show
free -h
```

Instalar limitando compilaci�n paralela:

```bash
export CMAKE_BUILD_PARALLEL_LEVEL=1
pip install face_recognition
```

Eliminar swap temporal despu�s de la instalaci�n:

```bash
sudo swapoff /var/swap
sudo rm /var/swap
```

Video de referencia utilizado:

https://www.youtube.com/watch?v=XNSSbSJ4lB4

---

## Entorno virtual

Crear entorno virtual:

```bash
python3 -m venv --system-site-packages .venv
```

Activar entorno:

```bash
source .venv/bin/activate
```

Importante:
- `--system-site-packages` es necesario para que el `.venv` pueda acceder a `picamera2` y OpenCV instalados por `apt`.

---

## Comprobaciones r�pidas

### Detectar c�maras disponibles

```bash
rpicam-hello --list-cameras
```

### Foto r�pida con preview de 5 segundos

```bash
rpicam-still -t 5000 -o foto_prueba.jpg
```

### Probar captura desde Python

```bash
python test_facial_capture.py
```

### Probar registro y verificaci�n facial

Registrar referencias:

```bash
python test_live_face_reference.py registrar
```

Verificar identidad:

```bash
python test_live_face_reference.py verificar
```

---

## Advertencias habituales

### QStandardPaths warning

Puede aparecer este mensaje:

```text
QStandardPaths: wrong permissions on runtime directory...
```

Importante:
- No impide que la c�mara funcione.
- Puede ignorarse si todo funciona correctamente.