# Sistema de Gestión de Guardias y Presencia

Aplicación desarrollada en Python utilizando Flask y SQLite para gestionar:

- Presencia del profesorado
- Reconocimiento facial
- Detección automática de ausencias
- Generación de guardias
- Asignación manual de coberturas
- Consulta de horarios semanales

El sistema simula el funcionamiento real de un centro educativo, diferenciando entre:

- planificación teórica (horario)
- situación real diaria (presencia)
- incidencias detectadas (ausencias)
- soluciones aplicadas (guardias)

---

# Tecnologías utilizadas

- Python 3
- Flask
- SQLite
- HTML + CSS
- Jinja2
- OpenCV
- face_recognition
- dlib
- Picamera2

---

# Funcionalidades principales

## Gestión de presencia

El sistema permite registrar entradas y salidas del profesorado durante cada hora lectiva.

La presencia se registra mediante reconocimiento facial utilizando Raspberry Pi Camera.

El sistema soporta:

- registro inicial de referencias faciales
- verificación facial en vivo
- detección automática de identidad
- registro automático de entrada/salida

---

## Reconocimiento facial

El sistema utiliza:

- `face_recognition`
- `dlib`
- `OpenCV`
- `Picamera2`

Flujo principal:

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
Registro automático de presencia
```

Cada profesor dispone de múltiples referencias faciales almacenadas para mejorar la precisión del reconocimiento.

---

## Detección automática de ausencias

El motor compara:

- el horario planificado
- la presencia real registrada

Cuando un profesor tiene clase pero no está presente, el sistema genera automáticamente una ausencia y crea una guardia pendiente de cubrir.

---

## Asignación de guardias

Las guardias pueden asignarse manualmente desde la interfaz web.

El sistema propone automáticamente profesores disponibles teniendo en cuenta:

- presencia actual
- profesores ocupados
- guardias ya asignadas
- ranking de prioridad

---

## Horarios semanales

Cada profesor puede consultar su horario semanal desde la vista `/horarios`.

La vista permite:

- seleccionar profesor
- consultar cualquier semana
- ver clases asignadas
- ver horas libres
- visualizar guardias reales asignadas

---

## Sistema de testing

La aplicación incorpora un modo test que permite simular:

- fechas concretas
- horas lectivas
- recreos
- fuera de horario

Esto facilita probar distintos escenarios sin depender de la hora real del sistema.

---

# Arquitectura general

El proyecto sigue una arquitectura modular:

- `app.py` → rutas Flask y coordinación general
- `config.py` → configuración global
- `modules/db` → acceso a datos
- `modules/guardias` → lógica de generación y ranking
- `modules/presencia` → control de presencia y reconocimiento facial
- `modules/horarios` → construcción de horarios
- `templates` → interfaz HTML
- `static` → recursos estáticos y referencias faciales

---

# Hardware utilizado

El sistema ha sido probado utilizando:

- Raspberry Pi 5
- Raspberry Pi OS
- Raspberry Pi Camera Module 3

---

# Estado actual

Actualmente el sistema permite:

- registrar presencia mediante reconocimiento facial
- generar guardias automáticamente
- asignar coberturas
- consultar horarios
- simular distintos escenarios mediante modo test
- integración completa con Raspberry Pi Camera

El sistema ya funciona integrado tanto a nivel software como hardware.