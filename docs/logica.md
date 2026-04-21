# Lógica del sistema

El sistema de guardias se basa en la comparación entre la planificación del centro y la situación real de los profesores en cada momento.

---

## Enfoque general

El objetivo es:

- Detectar qué clases quedan sin profesor
- Determinar qué profesores están disponibles
- Proponer candidatos para cubrir cada guardia
- Permitir la asignación manual desde la interfaz

---

## Arquitectura del sistema

El sistema sigue una arquitectura modular dividida en capas:

- **Capa de datos (`db`)**
  - `models.py`: define las clases que representan las entidades (Profesor, Guardia, etc.)
  - `db_manager.py`: gestiona el acceso a la base de datos y transforma las filas en objetos

- **Capa de lógica (`guardias`)**
  - `motor.py`: detecta ausencias y genera guardias
  - `reglas.py`: ordena profesores según criterios (ranking)

- **Capa de presentación (`Flask`)**
  - `app.py`: gestiona las rutas y coordina el sistema
  - Templates HTML: muestran la información al usuario

---

## Flujo de funcionamiento

El sistema sigue los siguientes pasos:

1. Obtener el horario del día
2. Consultar la presencia real de los profesores
3. Detectar ausencias
4. Generar guardias necesarias
5. Calcular profesores disponibles
6. Ordenar profesores según prioridad (ranking)
7. Permitir asignación manual desde la interfaz

---

## 1. Horario

Se consulta la tabla `horario`, que define qué profesor debería estar en cada aula y hora.

Solo se consideran las entradas con:

- tipo = "clase"

Esta información representa la planificación teórica del centro.

---

## 2. Presencia

Se consulta la tabla `presencia`, que indica qué profesores están presentes en cada hora del día.

Esto permite conocer la disponibilidad real de cada profesor en tiempo real.

---

## 3. Detección de ausencias

Un profesor se considera ausente cuando:

- Tiene una clase asignada en el horario
- No aparece como presente en esa hora

Cada ausencia se registra en la tabla `ausencias`.

---

## 4. Generación de guardias

Por cada ausencia detectada:

- Se crea una guardia
- Se registra el aula, la hora y el profesor ausente

Antes de crear una guardia, se comprueba si ya existe una para evitar duplicados.

---

## 5. Profesores disponibles

Un profesor se considera disponible cuando:

- Está presente en esa hora
- No tiene clase asignada en esa hora

Los profesores ocupados son aquellos que tienen:

- tipo = "clase" en esa hora

---

## 6. Ranking de profesores

Para cada guardia:

1. Se obtiene la lista de profesores disponibles
2. Se ordenan según criterios de prioridad

El resultado es una lista ordenada de candidatos para cubrir la guardia.

---

## Criterio de prioridad

Los profesores se ordenan por:

1. Menor número de guardias acumuladas
2. En caso de empate, menor ID de profesor

Esto garantiza un reparto equilibrado de las guardias.

---

## 7. Asignación de guardias

La asignación de guardias se realiza manualmente desde la interfaz web.

El sistema muestra:

- Profesores disponibles
- Ordenados según prioridad

El usuario selecciona el profesor que cubrirá la guardia.

Una vez asignada:

- Se registra el profesor que cubre
- Se incrementa su número de guardias

---

