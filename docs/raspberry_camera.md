# Raspberry Pi Camera y reconocimiento facial

Esta documentación describe la instalación y configuración del sistema de reconocimiento facial utilizado en el proyecto.

El sistema utiliza:

- Raspberry Pi Camera
- Picamera2
- OpenCV
- face_recognition
- dlib

---

# Hardware utilizado

El sistema ha sido probado utilizando:

- Raspberry Pi 5
- Raspberry Pi OS
- Raspberry Pi Camera Module 3

También debería funcionar con otros modelos compatibles con `Picamera2`.

---

# Arquitectura general

El flujo del reconocimiento facial es:

```text
Pi Camera
↓
Captura de imagen
↓
Detección facial
↓
Generación de encodings
↓
Comparación facial
↓
Registro automático de presencia
```

---

# Tecnologías utilizadas

## Picamera2

Se utiliza para controlar la cámara desde Python.

Ventajas:

- integración oficial con Raspberry Pi OS
- acceso rápido a frames
- soporte moderno para cámaras Raspberry

---

## OpenCV

Se utiliza principalmente para:

- conversión de imágenes
- procesamiento de frames
- compatibilidad con face_recognition

---

## face_recognition

Librería principal de reconocimiento facial.

Internamente utiliza:

- `dlib`
- embeddings faciales
- comparación de distancias faciales

---

# Instalación

## Instalar paquetes del sistema

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv cmake build-essential python3-dev
```

---

## Crear entorno virtual

Es importante utilizar `--system-site-packages` para poder acceder a `picamera2` y OpenCV instalados por `apt`.

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

---

## Instalar dependencias Python

```bash
pip install flask
pip install face_recognition
```

---

# Raspberry Pi con 4 GB de RAM

En Raspberry Pi con 4 GB de RAM, la instalación de `face_recognition` puede congelar el sistema porque compila `dlib`.

En ese caso, crear swap temporal antes de instalarlo.

---

## Crear swap temporal

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

---

## Instalar limitando compilación paralela

```bash
export CMAKE_BUILD_PARALLEL_LEVEL=1
pip install face_recognition
```

---

## Eliminar swap temporal

```bash
sudo swapoff /var/swap
sudo rm /var/swap
```

---

# Comprobaciones rápidas

## Detectar cámaras disponibles

```bash
rpicam-hello --list-cameras
```

---

## Captura rápida de imagen

```bash
rpicam-still -t 5000 -o foto_prueba.jpg
```

---

# Funcionamiento del sistema

## Primer registro

La primera vez que un profesor utiliza el sistema:

1. Se capturan múltiples referencias faciales
2. Se generan encodings faciales
3. Se almacenan en disco

El objetivo es mejorar la precisión del reconocimiento.

---

## Verificación posterior

En los siguientes accesos:

1. Se captura imagen en vivo
2. Se detecta la cara
3. Se compara con referencias almacenadas
4. Si coincide, se registra presencia

---

# Estructura de almacenamiento

Las referencias faciales se almacenan en:

```text
static/faces/
```

Cada profesor dispone de una carpeta propia:

```text
static/faces/profesor_X/
```

Dentro se almacena:

```text
encodings.pkl
```

que contiene múltiples encodings faciales serializados.

---

# Parámetros importantes

## Número de referencias

```python
NUM_REFERENCIAS_FACIALES = 5
```

Número de referencias faciales utilizadas durante el registro inicial.

---

## Tolerancia facial

```python
TOLERANCIA_RECONOCIMIENTO = 0.5
```

Valores menores:

- más estrictos
- menos falsos positivos

Valores mayores:

- más permisivos
- mayor riesgo de coincidencias incorrectas

---

# Problemas frecuentes

## `ModuleNotFoundError: No module named 'picamera2'`

Asegúrate de:

```bash
python3 -m venv --system-site-packages .venv
```

y de haber instalado:

```bash
sudo apt install -y python3-picamera2
```

---

## Instalación congelada

Si `face_recognition` congela la Raspberry:

- aumentar swap
- limitar compilación paralela

---

## Advertencia `QStandardPaths`

Puede aparecer:

```text
QStandardPaths: wrong permissions on runtime directory...
```

No suele afectar al funcionamiento de la cámara.

---

# Estado actual

Actualmente el sistema permite:

- registro facial inicial
- verificación facial en vivo
- integración con Flask
- integración completa con Raspberry Pi Camera
- registro automático de presencia