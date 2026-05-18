# Sistema de guardias

El módulo de guardias es el encargado de:

- detectar ausencias
- generar guardias automáticamente
- calcular profesores disponibles
- ordenar candidatos por prioridad
- permitir la asignación manual de coberturas

La lógica principal se encuentra en:

```text
modules/guardias/
```

---

# Objetivos del sistema

El sistema busca:

- detectar clases que quedan sin profesor
- generar guardias pendientes de cubrir
- proponer profesores disponibles
- repartir las guardias de forma equilibrada
- evitar duplicados
- impedir asignaciones fuera de horario o en horas pasadas

---

# Arquitectura del módulo

| Archivo | Responsabilidad |
|---|---|
| `motor.py` | Detección de ausencias, generación de guardias y disponibilidad |
| `reglas.py` | Ranking y ordenación de profesores |
| `models.py` | Clases de dominio relacionadas con guardias |

---

# Flujo general

```text
Horario planificado
↓
Presencia real
↓
Detección de ausencias
↓
Generación de guardias
↓
Cálculo de disponibles
↓
Ranking
↓
Asignación manual
```

---

# 1. Horario planificado

El sistema consulta la tabla `horario`.

Solo las entradas de tipo:

```text
clase
```

pueden generar una ausencia.

Las entradas de tipo:

```text
libre
```

representan profesores sin clase en esa hora.

---

# 2. Presencia real

La presencia real se obtiene desde el módulo de presencia.

Un profesor se considera presente si su último evento del día es:

```text
entrada
```

Si un profesor tiene clase y no está presente, se considera ausente.

---

# 3. Detección de ausencias

Una ausencia se genera cuando:

- un profesor tiene clase asignada
- el profesor no aparece como presente

La ausencia se almacena en la tabla:

```text
ausencias
```

---

# 4. Generación de guardias

Por cada ausencia detectada, el sistema crea una guardia.

Cada guardia almacena:

- fecha
- hora
- aula
- profesor ausente
- profesor que cubre, si ya está asignado

Antes de crear una guardia, el sistema comprueba si ya existe una equivalente para evitar duplicados.

---

# 5. Profesores disponibles

Un profesor puede cubrir una guardia si:

- está presente
- no tiene clase en esa hora
- no está ya cubriendo otra guardia en esa misma hora

Los profesores con clase se consideran ocupados.

---

# 6. Ranking de prioridad

El sistema ordena los profesores disponibles para proponer primero a los más adecuados.

Criterios utilizados:

1. Menor número de guardias acumuladas
2. Menor número de guardias en la semana actual
3. Menor carga lectiva semanal
4. Menor ID de profesor en caso de empate

Esto permite repartir las guardias de forma equilibrada.

---

# 7. Asignación de guardias

La asignación se realiza manualmente desde la vista:

```text
/guardias
```

El usuario selecciona un profesor de la lista propuesta.

Al asignar una guardia:

- se guarda el profesor que cubre
- se incrementan sus contadores de guardias
- la guardia deja de aparecer como pendiente

---

# Control de horas pasadas

El sistema evita asignar guardias en horas ya pasadas.

Ejemplo:

```python
HORA_TEST = 4
```

En este caso, las guardias de las horas 1, 2 y 3 quedan bloqueadas.

---

# Fuera de horario

Si la hora actual no corresponde a una hora lectiva:

```python
HORA_TEST = None
```

el sistema bloquea la asignación de guardias.

Esto evita asignaciones cuando el centro está fuera de horario o en recreo.

---

# Fechas pasadas

Si se consulta una fecha anterior a la actual:

- se muestran las guardias existentes
- no se permite asignar nuevas coberturas

---

# Modo test

El modo test permite simular fecha y hora desde `config.py`:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1
```

Esto permite probar escenarios como:

- primera hora
- horas pasadas
- fuera de horario
- fechas pasadas
- generación automática de guardias

---

# Integración con presencia

El módulo de guardias depende directamente del sistema de presencia.

La presencia determina:

- qué profesores están en el centro
- qué profesores faltan
- qué profesores pueden cubrir guardias

Sin presencia registrada, el sistema no puede saber quién está disponible realmente.

---

# Integración con horarios

El horario determina:

- qué profesor debería estar en clase
- qué aula queda descubierta
- qué profesores están ocupados

Por tanto, el motor compara:

```text
horario planificado + presencia real
```

para generar guardias.

---

# Integración con Flask

La vista principal es:

```text
/guardias
```

Desde ella se puede:

- elegir fecha
- ver guardias generadas
- consultar profesor ausente
- ver aula afectada
- asignar profesor disponible
- bloquear asignaciones no permitidas

---

# Validaciones del sistema

El sistema valida:

- que la guardia exista
- que no esté ya asignada
- que no sea una hora pasada
- que no sea fuera de horario
- que el profesor seleccionado sea válido
- que no se dupliquen guardias

---