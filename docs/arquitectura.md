# Arquitectura del sistema

El proyecto sigue una arquitectura modular basada en separación de responsabilidades.

Cada módulo se encarga de una parte concreta del sistema, facilitando:

- mantenimiento
- escalabilidad
- testing
- reutilización de código

---

# Arquitectura general

El sistema se divide en varias capas:

```text
Flask (interfaz web)
        ↓
Servicios y lógica de negocio
        ↓
Acceso a datos (SQLite)
        ↓
Integración hardware (Pi Camera)
```

---

# Estructura del proyecto

```text
project/
│
├── app.py
├── config.py
│
├── modules/
│   ├── db/
│   ├── guardias/
│   ├── horarios/
│   ├── presencia/
│   └── utils/
│
├── templates/
├── static/
│   └── faces/
│
└── test2.py
```

---

# app.py

Archivo principal de Flask.

Se encarga de:

- Definir rutas web
- Coordinar módulos
- Gestionar modo test
- Renderizar vistas HTML

Principales rutas:

| Ruta | Función |
|---|---|
| `/` | Página principal |
| `/presencia` | Gestión de presencia |
| `/guardias` | Gestión de guardias |
| `/horarios` | Consulta de horarios |

---

# config.py

Archivo central de configuración del proyecto.

Responsabilidad:

- Configuración global
- Variables de entorno
- Parámetros del reconocimiento facial
- Configuración de testing

Ejemplo:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1

NUM_REFERENCIAS_FACIALES = 5
TOLERANCIA_RECONOCIMIENTO = 0.5
```

---

# Módulo db

Ruta:

```text
modules/db/
```

Responsabilidad:

- Acceso a SQLite
- Consultas SQL
- Conversión de filas en objetos Python

Archivo principal:

```text
db_manager.py
```

Funciones típicas:

- crear profesores
- registrar presencia
- obtener horarios
- generar guardias
- asignar coberturas

---

# Módulo guardias

Ruta:

```text
modules/guardias/
```

Responsabilidad:

- Detectar ausencias
- Generar guardias
- Obtener profesores disponibles
- Aplicar ranking de prioridad

Archivos:

| Archivo | Función |
|---|---|
| `motor.py` | Lógica principal |
| `reglas.py` | Ranking y ordenación |
| `models.py` | Clases de dominio |

---

# Módulo presencia

Ruta:

```text
modules/presencia/
```

Responsabilidad:

- Registro de entradas y salidas
- Presencia actual
- Reconocimiento facial
- Integración con Pi Camera

Archivos principales:

| Archivo | Función |
|---|---|
| `registro.py` | Flujo principal de presencia |
| `facial.py` | Captura y verificación facial |

---

# Reconocimiento facial

El sistema utiliza:

- `face_recognition`
- `dlib`
- `OpenCV`
- `Picamera2`

Flujo:

```text
Primer registro
↓
Captura de múltiples referencias faciales
↓
Generación de encodings
↓
Guardado de referencias

Siguientes accesos
↓
Verificación facial en vivo
↓
Registro automático de entrada/salida
```

Las referencias faciales se almacenan en:

```text
static/faces/
```

Cada profesor dispone de:

```text
encodings.pkl
```

con múltiples referencias faciales registradas.

---

# Módulo horarios

Ruta:

```text
modules/horarios/
```

Responsabilidad:

- Construcción de horarios
- Mezcla de horario fijo y guardias
- Generación de tablas para interfaz

Archivo principal:

```text
servicio.py
```

---

# Módulo utils

Ruta:

```text
modules/utils/
```

Responsabilidad:

- Funciones auxiliares
- Gestión temporal
- Horas lectivas
- Utilidades comunes

---

# Base de datos

El sistema utiliza SQLite como motor de persistencia.

Ventajas:

- ligero
- simple
- sin servidor externo
- fácil despliegue
- adecuado para Raspberry Pi

---

# Interfaz web

La interfaz utiliza:

- Flask
- Jinja2
- HTML
- CSS
- JavaScript

La aplicación utiliza renderizado server-side mediante plantillas.

---

# Modo test

El sistema incorpora testing integrado mediante configuración.

Ejemplo:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1
```

Permite simular:

- horas pasadas
- recreos
- fuera de horario
- fechas futuras
- generación de guardias

sin depender de la hora real del sistema.

---

# Flujo principal del sistema

## 1. Horario

El sistema consulta el horario semanal planificado.

---

## 2. Presencia

Se obtiene la presencia real registrada mediante reconocimiento facial.

---

## 3. Ausencias

Se detectan profesores con clase que no están presentes.

---

## 4. Guardias

Se generan guardias automáticamente.

---

## 5. Ranking

Se calculan profesores disponibles y se ordenan por prioridad.

---

## 6. Asignación

El usuario asigna manualmente la cobertura desde la interfaz web.

---

# Decisiones de diseño

## Separación entre planificación y realidad

El sistema diferencia claramente entre:

- horario teórico
- presencia real
- incidencias
- coberturas

---

## Arquitectura modular

Cada responsabilidad se encuentra aislada en un módulo específico.

Esto evita mezclar:

- lógica de negocio
- acceso a datos
- interfaz
- reconocimiento facial

---

## Validación backend + frontend

Las restricciones importantes se validan tanto:

- visualmente en la interfaz
- como internamente en Flask

Ejemplos:

- bloqueo fuera de horario
- bloqueo de guardias pasadas
- verificación facial obligatoria