# Sistema de presencia

El módulo de presencia es el encargado de gestionar:

- entradas y salidas del profesorado
- verificación de identidad
- reconocimiento facial
- presencia actual
- integración con Raspberry Pi Camera

La lógica principal se encuentra en:

```text
modules/presencia/
```

---

# Objetivos del sistema

El sistema busca:

- automatizar el registro de presencia
- evitar registros manuales incorrectos
- verificar identidad mediante reconocimiento facial
- conocer qué profesores están presentes en tiempo real
- servir de base para la generación automática de guardias

---

# Arquitectura del módulo

El módulo se divide principalmente en dos partes:

| Archivo | Responsabilidad |
|---|---|
| `registro.py` | Lógica principal de presencia |
| `facial.py` | Reconocimiento facial y cámara |

---

# Flujo general

El funcionamiento principal es:

```text
Profesor
↓
Verificación facial
↓
Registro entrada/salida
↓
Actualización presencia actual
↓
Detección automática de ausencias
```

---

# Primer registro facial

La primera vez que un profesor utiliza el sistema:

1. Se abre la cámara
2. Se capturan múltiples referencias faciales
3. Se generan encodings faciales
4. Se almacenan en disco

El objetivo es mejorar la precisión del reconocimiento.

---

## Captura de referencias

El sistema solicita al usuario:

- mirar de frente
- cambiar ligeramente el ángulo
- mantener buena iluminación

Actualmente se utilizan:

```python
NUM_REFERENCIAS_FACIALES = 5
```

---

# Almacenamiento facial

Las referencias se almacenan en:

```text
static/faces/
```

Cada profesor dispone de una carpeta:

```text
static/faces/profesor_X/
```

Dentro se almacena:

```text
encodings.pkl
```

que contiene múltiples encodings faciales serializados.

---

# Verificación facial

En accesos posteriores:

1. Se abre la cámara
2. Se captura imagen en vivo
3. Se detecta el rostro
4. Se generan encodings temporales
5. Se comparan con referencias guardadas

Si la comparación es válida:

```text
Profesor reconocido
```

y se registra presencia automáticamente.

---

# Librerías utilizadas

El sistema utiliza:

- `face_recognition`
- `dlib`
- `OpenCV`
- `Picamera2`

---

# Tolerancia de reconocimiento

La comparación facial utiliza:

```python
TOLERANCIA_RECONOCIMIENTO = 0.5
```

## Funcionamiento

El sistema calcula distancia facial:

- valores bajos → caras más parecidas
- valores altos → caras diferentes

---

## Valores habituales

| Distancia | Resultado aproximado |
|---|---|
| 0.2 - 0.4 | Muy probable misma persona |
| 0.5 | Coincidencia aceptable |
| 0.6+ | Riesgo de falsos positivos |

---

# Registro de presencia

Tras validación facial correcta:

1. Se obtiene el historial del profesor
2. Se analiza el último evento registrado
3. Se decide automáticamente:

```text
entrada
```

o

```text
salida
```

---

# Lógica de entrada/salida

## Primer evento del día

Si no existen eventos previos:

```text
entrada
```

---

## Evento anterior = entrada

El nuevo evento será:

```text
salida
```

---

## Evento anterior = salida

El nuevo evento será:

```text
entrada
```

---

# Prevención de duplicados

El sistema evita:

- múltiples registros en la misma hora
- entradas repetidas
- salidas repetidas

Antes de registrar presencia se comprueba:

- profesor
- fecha
- hora

---

# Presencia actual

Un profesor se considera presente cuando:

```text
su último evento es "entrada"
```

Esto permite:

- entradas y salidas múltiples
- abandonar temporalmente el centro
- volver a entrar posteriormente

---

# Integración con guardias

La presencia real se utiliza posteriormente para:

- detectar ausencias
- generar guardias automáticamente
- calcular profesores disponibles

---

# Integración con Flask

La interfaz web permite:

- seleccionar profesor
- iniciar verificación facial
- registrar entrada/salida
- visualizar historial de presencia

La vista principal es:

```text
/presencia
```

---

# Validaciones del sistema

El sistema protege tanto frontend como backend.

Ejemplos:

- bloqueo fuera de horario
- verificación facial obligatoria
- prevención de duplicados
- control de horarios válidos

---

# Configuración importante

Parámetros principales en `config.py`:

```python
NUM_REFERENCIAS_FACIALES = 5
MAX_INTENTOS_REFERENCIA = 15
TOLERANCIA_RECONOCIMIENTO = 0.5
TIEMPO_VERIFICACION_FACIAL = 10
```

---