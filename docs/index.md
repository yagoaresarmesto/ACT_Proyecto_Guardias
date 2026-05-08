# Sistema de Gestión de Guardias y Presencia

Aplicación desarrollada en Python utilizando Flask y SQLite para gestionar:

- Presencia del profesorado
- Detección automática de ausencias
- Generación de guardias
- Asignación manual de coberturas
- Consulta de horarios semanales

El sistema simula el funcionamiento real de un centro educativo, diferenciando entre:

- Planificación teórica (horario)
- Situación real diaria (presencia)
- Incidencias detectadas (ausencias)
- Soluciones aplicadas (guardias)

---

# Tecnologías utilizadas

- Python 3
- Flask
- SQLite
- HTML + CSS
- Jinja2

---

# Funcionalidades principales

## Gestión de presencia

El sistema permite registrar entradas y salidas del profesorado durante cada hora lectiva.

La presencia se utiliza posteriormente para detectar automáticamente qué profesores están ausentes.

---

## Detección automática de ausencias

El motor compara:

- El horario planificado
- La presencia real registrada

Cuando un profesor tiene clase pero no está presente, el sistema genera automáticamente una ausencia y crea una guardia pendiente de cubrir.

---

## Asignación de guardias

Las guardias pueden asignarse manualmente desde la interfaz web.

El sistema propone automáticamente profesores disponibles teniendo en cuenta:

- Presencia actual
- Profesores ocupados
- Guardias ya asignadas
- Ranking de prioridad

---

## Horarios semanales

Cada profesor puede consultar su horario semanal desde la vista `/horarios`.

La vista permite:

- Seleccionar profesor
- Consultar cualquier semana
- Ver clases asignadas
- Ver horas libres
- Visualizar guardias reales asignadas

---

## Sistema de testing

La aplicación incorpora un modo test que permite simular:

- Fechas concretas
- Horas lectivas
- Recreos
- Fuera de horario

Esto facilita probar distintos escenarios sin depender de la hora real del sistema.

---

# Arquitectura general

El proyecto sigue una arquitectura modular:

- `app.py` → rutas Flask y coordinación general
- `modules/db` → acceso a datos
- `modules/guardias` → lógica de generación y ranking
- `modules/presencia` → control de presencia
- `modules/horarios` → construcción de horarios
- `templates` → interfaz HTML
- `static` → estilos CSS

---

# Estado actual

Actualmente el sistema permite:

- Registrar presencia manualmente
- Generar guardias automáticamente
- Asignar coberturas
- Consultar horarios
- Simular distintos escenarios mediante modo test

El siguiente objetivo del proyecto es integrar registro automático de presencia mediante hardware externo (Pi Camera).