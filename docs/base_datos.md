# Base de datos

El sistema utiliza una base de datos relacional SQLite para modelar la gestión de presencia, ausencias y guardias de un centro educativo.

La base de datos separa claramente:

- planificación teórica
- presencia real
- incidencias detectadas
- coberturas realizadas

---

# Modelo general

El flujo principal del sistema es:

```text
Horario → Presencia → Ausencias → Guardias
```

## Horario

Representa la planificación semanal del profesorado.

---

## Presencia

Representa la situación real del profesorado en cada momento.

---

## Ausencias

Se detectan automáticamente cuando un profesor con clase no aparece como presente.

---

## Guardias

Se generan automáticamente para cubrir las ausencias detectadas.

---

# Tablas

## profesores

Almacena la información básica del profesorado.

| Campo | Tipo | Descripción |
|---|---|---|
| id_profesor | INTEGER | Identificador único |
| nombre | TEXT | Nombre del profesor |
| departamento | TEXT | Departamento |
| rfid_uid | TEXT | Identificador RFID opcional |
| guardias_semana | INTEGER | Número de guardias en la semana |
| guardias_acumuladas | INTEGER | Total histórico de guardias |

---

## horario

Define el horario semanal planificado.

| Campo | Tipo | Descripción |
|---|---|---|
| id_horario | INTEGER | Identificador |
| id_profesor | INTEGER | Profesor asignado |
| dia_semana | INTEGER | Día de la semana (1-5) |
| hora | INTEGER | Hora lectiva |
| tipo | TEXT | Tipo de bloque |
| aula | TEXT | Aula o grupo |

### Tipos actuales utilizados

Actualmente el sistema utiliza principalmente:

- `clase`
- `libre`

El tipo `guardia` sigue soportado por la base de datos, aunque no se utiliza activamente en la lógica actual.

---

## presencia

Registra entradas y salidas del profesorado.

| Campo | Tipo | Descripción |
|---|---|---|
| id_presencia | INTEGER | Identificador |
| id_profesor | INTEGER | Profesor |
| fecha | DATE | Fecha |
| hora | INTEGER | Hora lectiva |
| tipo | TEXT | `entrada` o `salida` |

La presencia se calcula interpretando el último evento registrado de cada profesor.

Esto permite modelar entradas y salidas durante la jornada.

---

## ausencias

Registra las ausencias detectadas automáticamente.

| Campo | Tipo | Descripción |
|---|---|---|
| id_ausencia | INTEGER | Identificador |
| id_profesor | INTEGER | Profesor ausente |
| fecha | DATE | Fecha |
| hora | INTEGER | Hora |

Las ausencias se generan comparando:

- horario planificado
- presencia real

---

## guardias

Gestiona las coberturas de ausencias.

| Campo | Tipo | Descripción |
|---|---|---|
| id_guardia | INTEGER | Identificador |
| fecha | DATE | Fecha |
| hora | INTEGER | Hora |
| aula | TEXT | Aula afectada |
| id_profesor_ausente | INTEGER | Profesor ausente |
| id_profesor_cubre | INTEGER | Profesor que cubre |

Una guardia puede existir inicialmente sin profesor asignado.

---

# Relaciones principales

## profesores ↔ horario

Un profesor puede tener múltiples bloques horarios.

---

## profesores ↔ presencia

Un profesor puede registrar múltiples eventos de presencia.

---

## profesores ↔ ausencias

Una ausencia pertenece a un profesor concreto.

---

## profesores ↔ guardias

La tabla guardias relaciona:

- profesor ausente
- profesor que cubre

---

# Funcionamiento del sistema

## 1. Consulta de horario

El sistema obtiene el horario del día correspondiente.

---

## 2. Consulta de presencia

Se obtiene la lista de profesores presentes.

---

## 3. Detección de ausencias

Si un profesor:

- tiene clase
- y no está presente

se genera una ausencia.

---

## 4. Generación de guardias

Por cada ausencia detectada:

- se crea una guardia
- se almacena aula y hora afectada

---

## 5. Asignación de cobertura

El sistema propone profesores disponibles y permite asignar manualmente la cobertura.

---

# Decisiones de diseño

## Separación entre planificación y realidad

La tabla `horario` representa la planificación teórica.

La tabla `presencia` representa la situación real.

Esto permite detectar incidencias automáticamente.

---

## Registro histórico

Las guardias y ausencias quedan almacenadas para permitir:

- estadísticas
- trazabilidad
- análisis posterior

---

## Flexibilidad del sistema

La estructura permite futuras ampliaciones como:

- RFID
- reconocimiento facial
- integración hardware
- automatización de presencia

---

# Integridad de datos

El sistema utiliza:

- claves foráneas
- restricciones `CHECK`
- validaciones desde Flask
- control de duplicados en guardias

---

# Estado actual

Actualmente la base de datos soporta:

- gestión de horarios
- registro de presencia
- generación automática de guardias
- ranking de profesores
- visualización de horarios semanales

El siguiente paso previsto es integrar presencia automática mediante hardware externo.