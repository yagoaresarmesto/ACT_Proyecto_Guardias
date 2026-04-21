# Lógica del sistema

El sistema de guardias se basa en la comparación entre la planificación del centro y la situación real de los profesores en cada momento.

---

## Enfoque general

El objetivo es:

- Detectar qué clases quedan sin profesor
- Determinar qué profesores están disponibles
- Asignar automáticamente quién cubre cada guardia

---

##  Flujo de funcionamiento

El sistema sigue los siguientes pasos:

1. Obtener el horario del día
2. Consultar la presencia real de los profesores
3. Detectar ausencias
4. Generar guardias necesarias
5. Calcular profesores disponibles
6. Asignar guardias automáticamente

---

##  1. Horario

Se consulta la tabla `horario`, que define qué profesor debería estar en cada aula y hora.

Solo se consideran las entradas con:


Esta información representa la planificación teórica del centro.

---

##  2. Presencia

Se consulta la tabla `presencia`, que indica qué profesores están presentes en cada hora del día.

Esto permite conocer la disponibilidad real de cada profesor en tiempo real.

---

## 3. Detección de ausencias

Un profesor se considera ausente cuando:

- Tiene una clase asignada en el horario
- No aparece como presente en esa hora


Cada ausencia se registra en la tabla `ausencias`.

---

##  4. Generación de guardias

Por cada ausencia detectada:

- Se crea una guardia
- Se registra el aula, la hora y el profesor ausente

Antes de crear una guardia, se comprueba si ya existe una para evitar duplicados.

La condición utilizada es:



---

##  5. Profesores disponibles

Un profesor se considera disponible cuando:

- Está presente en esa hora
- No tiene clase asignada en esa hora


Los profesores ocupados son aquellos que tienen: tipo = clase


---

## 6. Asignación de guardias

Para cada guardia sin cubrir:

1. Se obtiene la lista de profesores disponibles
2. Se ordenan según criterios de prioridad
3. Se selecciona el profesor con mayor prioridad
4. Se asigna la guardia

---

## Criterio de prioridad

Los profesores se ordenan por:

1. Menor número de guardias acumuladas
2. En caso de empate, menor ID de profesor

Esto garantiza un reparto equilibrado de las guardias.

---

## Consideraciones

- Si no hay profesores disponibles, la guardia queda pendiente
- El sistema depende de la presencia real en cada hora
- Las guardias pueden asignarse automáticamente o manualmente
- El sistema evita duplicados en la generación de guardias

---

## Resultado

El sistema genera una lista de guardias que incluye:

- Aula
- Hora
- Profesor ausente
- Profesor asignado (si existe)

Esto permite visualizar rápidamente las incidencias del centro y gestionar la cobertura de clases.
