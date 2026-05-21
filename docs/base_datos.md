# Base de datos

El sistema utiliza SQLite como base de datos relacional para gestionar:

- horarios
- presencia
- ausencias
- guardias
- reconocimiento facial

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

La presencia se registra mediante reconocimiento facial utilizando Raspberry Pi Camera.

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
| rfid_uid | TEXT | Ruta a referencias faciales |
| guardias_semana | INTEGER | Número de guardias en la semana |
| guardias_acumuladas | INTEGER | Total histórico de guardias |

### Observación

Se llama `rfid_uid` puede confundir el nombre, no es más conveniente.

Actualmente se reutiliza para almacenar la ruta al archivo de referencias faciales (`encodings.pkl`).

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

El tipo `guardia` sigue soportado por la base de datos, aunque no se utiliza activamente en la lógica actual, ya que consideré que está distinción puede ser confusa.

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

La tabla `guardias` relaciona:

- profesor ausente
- profesor que cubre

---

# Reconocimiento facial

El reconocimiento facial funciona mediante:

- `face_recognition`
- `dlib`
- `OpenCV`
- `Picamera2`

Cada profesor dispone de múltiples referencias de caras.

Las referencias se almacenan en:

```text
static/faces/
```

Cada carpeta de profesor contiene:

```text
encodings.pkl
```

El sistema utiliza múltiples encodings para mejorar la robustez del reconocimiento.

---

# Funcionamiento del sistema

## 1. Consulta de horario

El sistema obtiene el horario del día correspondiente.

---

## 2. Verificación facial

El profesor se identifica mediante reconocimiento facial en vivo.

---

## 3. Registro de presencia

Si la identidad coincide:

- se registra entrada o salida automáticamente

---

## 4. Detección de ausencias

Si un profesor:

- tiene clase
- y no aparece como presente

se genera una ausencia.

---

## 5. Generación de guardias

Por cada ausencia detectada:

- se crea una guardia
- se almacena aula y hora afectada

---

## 6. Asignación de cobertura

El sistema propone profesores disponibles y permite asignar manualmente la cobertura.

---

# Decisiones de diseño

## Separación entre planificación y realidad

La tabla `horario` representa la planificación teórica.

La tabla `presencia` representa la situación real.

Esto permite detectar incidencias automáticamente.

---

## Arquitectura modular

La lógica se separa en módulos independientes:

- presencia
- guardias
- horarios
- reconocimiento facial
- acceso a datos

---

## Registro histórico

Las guardias y ausencias quedan almacenadas para permitir:

- estadísticas
- trazabilidad
- análisis posterior

---

## Flexibilidad del sistema

La estructura permite futuras ampliaciones como:

- RFID real
- múltiples cámaras
- reconocimiento distribuido
- estadísticas avanzadas
- automatización completa

---

# Integridad de datos

El sistema utiliza:

- claves foráneas
- restricciones `CHECK`
- validaciones desde Flask
- control de duplicados
- verificación facial obligatoria