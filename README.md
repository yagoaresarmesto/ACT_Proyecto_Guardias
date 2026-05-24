# ACT Proyecto Guardias

Aplicación Flask para gestionar presencia del profesorado, guardias y reconocimiento facial con Raspberry Pi Camera.

---

## Requisitos

- Raspberry Pi 5
- Raspberry Pi OS
- Camera Module compatible, preferiblemente Camera Module 3, que es la que se ha probado
- Python 3
- Git

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/yagoaresarmesto/ACT_Proyecto_Guardias.git
cd ACT_Proyecto_Guardias
```

---

## 2. Instalar paquetes del sistema

Se instalan por `apt` los paquetes relacionados con cámara, OpenCV y compilación de dependencias.

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv cmake build-essential python3-dev
```

`picamera2` y OpenCV se instalan en el sistema porque funcionan mejor así en Raspberry Pi.

---

## 3. Crear entorno virtual

Es importante usar `--system-site-packages` para que el entorno pueda acceder a `picamera2` y OpenCV instalados por `apt`.

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

---

## 4. Instalar dependencias Python

Con el entorno virtual activado, instalar Flask:

```bash
pip install flask
```

Después instalar `face_recognition`: suele tardar entre 10-20 minutos que compila dlib

```bash
pip install face_recognition
```

### Raspberry Pi con 4 GB de RAM

En Raspberry Pi con 4 GB de RAM, la instalación de `face_recognition` puede congelar el sistema porque compila `dlib`.

En ese caso, crear swap temporal antes de instalarlo.

Crear swap temporal de 4 GB:

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

Instalar `face_recognition` limitando la compilación paralela:

```bash
export CMAKE_BUILD_PARALLEL_LEVEL=1
pip install face_recognition
```

Eliminar swap temporal después de la instalación:

```bash
sudo swapoff /var/swap
sudo rm /var/swap
```

En Raspberry Pi 5 con 8 GB de RAM normalmente no es necesario crear swap adicional.

---

## 5. Comprobar cámara

Detectar cámaras disponibles:

```bash
rpicam-hello --list-cameras
```

Prueba rápida de captura con preview de 5 segundos:

```bash
rpicam-still -t 5000 -o foto_prueba.jpg
```

---

## 6. Inicializar base de datos

```bash
python -m modules.db.init_db
```

Opcionalmente cargar datos de prueba:

```bash
python cargar_datos.py
```

---

## 7. Ejecutar aplicación

```bash
python app.py
```

Abrir en navegador:

```text
http://127.0.0.1:5000
```

---

## Problemas frecuentes

### `ModuleNotFoundError: No module named 'picamera2'`

Asegúrate de haber creado el entorno con:

```bash
python3 -m venv --system-site-packages .venv
```

y de haber instalado:

```bash
sudo apt install -y python3-picamera2
```

---

### La instalación de `face_recognition` congela la Raspberry

Crear swap temporal y limitar compilación:

```bash
sudo fallocate -l 4G /var/swap
sudo chmod 600 /var/swap
sudo mkswap /var/swap
sudo swapon /var/swap

export CMAKE_BUILD_PARALLEL_LEVEL=1
pip install face_recognition
```

Después eliminar la swap temporal:

```bash
sudo swapoff /var/swap
sudo rm /var/swap
```

---

### Advertencia `QStandardPaths`

Puede aparecer:

```text
QStandardPaths: wrong permissions on runtime directory...
```

Si la cámara funciona correctamente, se puede ignorar.
