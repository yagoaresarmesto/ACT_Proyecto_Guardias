# Base de datos

El sistema se basa en una base de datos relacional en SQLite que modela la gestión de guardias en un centro educativo.

Se han definido varias tablas que representan la planificación, la realidad diaria y la gestión de incidencias.

---

##  Modelo general

El flujo del sistema es:

Horario → Presencia → Ausencias → Guardias

- **Horario**: planificación del centro
- **Presencia**: qué profesores están realmente
- **Ausencias**: detección de fallos en el horario
- **Guardias**: solución a las ausencias

---

##  Tablas

###  profesores

Almacena la información básica de los profesores.

| Campo | Tipo | Descripción |
|------|-----|------------|
| id_profesor | INTEGER | Identificador único |
| nombre | TEXT | Nombre del profesor |
| departamento | TEXT | Departamento |
| rfid_uid | TEXT | Identificador RFID (opcional) |
| guardias_semana | INTEGER | Guardias en la semana |
| guardias_acumuladas | INTEGER | Total histórico |

---

###  horario

Define la planificación semanal del centro.

| Campo | Tipo | Descripción |
|------|-----|------------|
| id_horario | INTEGER | ID |
| id_profesor | INTEGER | Profesor asignado |
| dia_semana | INTEGER | Día (1-5) |
| hora | INTEGER | Hora lectiva |
| tipo | TEXT | 'clase', 'guardia' o 'libre' |
| aula | TEXT | Aula |

📌 Esta tabla representa lo que *debería ocurrir*.

---

###  presencia

Registra la presencia real de los profesores.

| Campo | Tipo | Descripción |
|------|-----|------------|
| id_presencia | INTEGER | ID |
| id_profesor | INTEGER | Profesor |
| fecha | DATE | Día concreto |
| hora | INTEGER | Hora |
| presente | BOOLEAN | 1 = presente |

 Permite saber quién está disponible en cada momento.

---

### ❌ ausencias

Registra las ausencias detectadas.

| Campo | Tipo | Descripción |
|------|-----|------------|
| id_ausencia | INTEGER | ID |
| id_profesor | INTEGER | Profesor ausente |
| fecha | DATE | Fecha |
| hora | INTEGER | Hora |

Se genera automáticamente a partir del horario y la presencia.

---

### 🛠 guardias

Gestiona la cobertura de ausencias.

| Campo | Tipo | Descripción |
|------|-----|------------|
| id_guardia | INTEGER | ID |
| fecha | DATE | Fecha |
| hora | INTEGER | Hora |
| aula | TEXT | Aula |
| id_profesor_ausente | INTEGER | Profesor que falta |
| id_profesor_cubre | INTEGER | Profesor que cubre |

 Representa tanto el problema (ausencia) como la solución (cobertura).

---

## Funcionamiento del sistema

1. Se consulta el horario del día
2. Se compara con la presencia real
3. Se detectan ausencias
4. Se generan guardias
5. Se asignan profesores disponibles

---

##  Decisiones de diseño

- Separación entre planificación (`horario`) y realidad (`presencia`)
- Las ausencias se almacenan para facilitar consultas
- Las guardias contienen tanto el profesor ausente como el que cubre
- Se evita duplicar información innecesaria

---

## Integridad

- Uso de claves foráneas entre tablas
- Control de valores mediante `CHECK`
- Posibilidad de evitar duplicados en guardias mediante índices únicos