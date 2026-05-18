# Sistema de horarios

El módulo de horarios permite consultar el horario semanal de cada profesor.

La lógica principal se encuentra en:

```text
modules/horarios/
```

---

# Objetivos del sistema

El sistema busca:

- mostrar el horario semanal del profesorado
- diferenciar clases y horas libres
- consultar horarios por profesor
- consultar semanas concretas
- mostrar guardias reales asignadas dentro de la semana

---

# Arquitectura del módulo

| Archivo | Responsabilidad |
|---|---|
| `servicio.py` | Construcción de la tabla semanal de horarios |

---

# Vista principal

La vista principal del módulo es:

```text
/horarios
```

Desde esta vista se puede:

- seleccionar profesor
- seleccionar fecha
- visualizar la semana completa
- consultar clases
- consultar horas libres
- ver guardias reales asignadas

---

# Funcionamiento general

El sistema construye una tabla semanal con:

```text
lunes → viernes
1ª hora → 10ª hora
```

Cada celda puede mostrar:

- clase asignada
- hora libre
- guardia real asignada

---

# Horario fijo

El horario fijo procede de la tabla:

```text
horario
```

Este horario depende únicamente de:

- profesor
- día de la semana
- hora

No depende de una fecha concreta.

Por eso, si se cambia de semana, el horario base del profesor se mantiene igual.

---

# Fecha seleccionada

La vista permite seleccionar una fecha.

Esa fecha se utiliza para calcular la semana completa:

```text
lunes → viernes
```

Por ejemplo:

```text
2026-05-04
```

genera la semana:

```text
2026-05-04 → 2026-05-08
```

Si se selecciona otro día dentro de la misma semana, la tabla mostrada será la misma.

---

# Guardias reales

A diferencia del horario fijo, las guardias reales sí dependen de fechas concretas.

Una guardia real aparece en el horario de un profesor cuando:

- existe una guardia generada
- está asignada a ese profesor
- pertenece a la semana seleccionada

Esto permite ver en el horario semanal si un profesor ha cubierto alguna guardia concreta.

---

# Diferencia entre horario y guardias reales

## Horario fijo

Representa la planificación semanal normal.

Ejemplo:

```text
1ESO-A / Aula 102
Libre
```

---

## Guardia real

Representa una cobertura concreta generada por una ausencia.

Ejemplo:

```text
Guardia real: 2ESO-B / Aula 203
```

---

# Clases

Las clases se obtienen desde la tabla `horario`.

Una clase contiene:

- curso o grupo
- aula

Ejemplo:

```text
1ESO-A / Aula 102
```

---

# Horas libres

Las horas libres indican que el profesor no tiene clase asignada en esa hora.

En la interfaz se muestran como:

```text
Libre
```

Estas horas pueden servir para saber si el profesor podría estar disponible para cubrir guardias, siempre que también esté presente.

---

# Construcción de la tabla

El servicio construye una estructura similar a:

```python
tabla[hora][dia]
```

Ejemplo:

```python
tabla[1][1]  # lunes, primera hora
tabla[3][5]  # viernes, tercera hora
```

Esto permite renderizar fácilmente la tabla en HTML.

---

# Integración con guardias

El módulo de horarios consulta guardias asignadas entre:

```text
fecha_inicio_semana
fecha_fin_semana
```

Si una guardia está asignada al profesor seleccionado, se añade a la celda correspondiente.

---

# Integración con Flask

La ruta `/horarios` recibe:

- profesor seleccionado
- fecha seleccionada

Y devuelve a la plantilla:

- tabla semanal
- días
- horas
- rango de fechas de la semana
- tramos horarios

---

# Integración con presencia

El módulo de horarios no registra presencia directamente.

Sin embargo, se relaciona con presencia porque:

- las guardias reales dependen de ausencias
- las ausencias dependen de presencia
- las guardias asignadas pueden aparecer en el horario del profesor

---

# Modo test

El modo test afecta a la fecha inicial que aparece en la vista.

Desde `config.py` se puede definir:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-04"
```

Cuando el modo test está activo, la vista puede abrir directamente sobre la fecha simulada.

---

# Validaciones

El módulo debe soportar:

- profesor no seleccionado
- fecha sin guardias reales
- semanas sin incidencias
- profesores sin horario completo
- guardias reales solo si están asignadas

---