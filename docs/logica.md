# Lógica del sistema

El sistema de gestión de guardias se basa en comparar:

- la planificación teórica del centro
- la situación real del profesorado

A partir de esa comparación, el sistema detecta automáticamente incidencias y genera las guardias necesarias.

La presencia se obtiene mediante reconocimiento facial utilizando Raspberry Pi Camera.

---

# Objetivos del sistema

El sistema busca:

- detectar clases sin profesor
- verificar identidad mediante reconocimiento facial
- determinar qué profesores están disponibles
- generar guardias automáticamente
- proponer candidatos ordenados por prioridad
- permitir asignación manual desde la interfaz web

---

# Arquitectura lógica

El sistema se divide en varias capas funcionales.

---

## Capa de datos (`db`)

Responsable de:

- consultas SQL
- persistencia
- transformación de datos

Archivo principal:

```text
db_manager.py
```

---

## Capa de lógica (`guardias`)

Responsable de:

- detectar ausencias
- generar guardias
- calcular disponibilidad
- aplicar ranking

Archivos principales:

```text
motor.py
reglas.py
```

---

## Capa de presencia (`presencia`)

Responsable de:

- registrar entradas y salidas
- calcular presencia actual
- determinar profesores presentes
- reconocimiento facial
- integración con Pi Camera

Archivos principales:

```text
registro.py
facial.py
```

---

## Capa de horarios (`horarios`)

Responsable de:

- construir horarios semanales
- mezclar horarios fijos y guardias reales
- preparar tablas para la interfaz

Archivo principal:

```text
servicio.py
```

---

## Capa de presentación (`Flask`)

Responsable de:

- rutas web
- renderizado HTML
- interacción con el usuario

Archivo principal:

```text
app.py
```

---

# Flujo general del sistema

El funcionamiento principal sigue este orden:

```text
Horario
↓
Verificación facial
↓
Presencia
↓
Ausencias
↓
Guardias
↓
Ranking
↓
Asignación
```

---

# 1. Horario

El sistema consulta el horario semanal planificado.

La tabla `horario` contiene:

- profesor
- día
- hora
- tipo
- aula

Actualmente se utilizan principalmente:

- `clase`
- `libre`

Solo las entradas `clase` generan posibles ausencias.

---

# 2. Verificación facial

El profesor se identifica mediante reconocimiento facial en vivo.

El sistema utiliza:

- `face_recognition`
- `dlib`
- `OpenCV`
- `Picamera2`

## Primer registro

La primera vez:

1. Se capturan múltiples referencias faciales
2. Se generan encodings
3. Se almacenan en disco

Cada profesor dispone de varias referencias para mejorar la precisión.

---

## Verificación posterior

En los siguientes accesos:

1. La cámara captura imagen en vivo
2. Se detecta el rostro
3. Se comparan encodings faciales
4. Si coincide, se registra presencia

---

# 3. Presencia

La presencia se basa en eventos de:

- entrada
- salida

Cada profesor puede registrar múltiples eventos durante el día.

El sistema considera presente a un profesor cuando su último evento es:

```text
entrada
```

El registro de presencia se realiza automáticamente tras validación facial correcta.

---

# 4. Detección de ausencias

Un profesor se considera ausente cuando:

- tiene una clase planificada
- no aparece como presente

Las ausencias se generan automáticamente desde `motor.py`.

---

# 5. Generación de guardias

Por cada ausencia detectada:

- se crea una guardia
- se almacena aula y hora
- se registra el profesor ausente

Antes de crearla, el sistema comprueba si ya existe una guardia equivalente para evitar duplicados.

---

# 6. Profesores disponibles

Un profesor se considera disponible cuando:

- está presente
- no tiene clase en esa hora
- no está cubriendo ya otra guardia

Los profesores ocupados son aquellos que tienen:

```text
tipo = "clase"
```

en esa hora.

---

# 7. Ranking de prioridad

Para cada guardia:

1. Se obtiene la lista de profesores disponibles
2. Se aplica un sistema de prioridad

El resultado es una lista ordenada de candidatos.

---

# Criterios de prioridad

Los profesores se ordenan por:

1. menor número de guardias acumuladas
2. menor número de guardias en la semana actual
3. menor carga lectiva semanal
4. menor ID de profesor en caso de empate

Esto permite repartir las guardias de forma equilibrada.

---

# 8. Asignación de guardias

La asignación se realiza manualmente desde la interfaz web.

El sistema muestra:

- guardias pendientes
- profesores disponibles
- ranking ordenado

Cuando una guardia se asigna:

- se registra el profesor que cubre
- se actualizan sus contadores

---

# Horarios semanales

La vista `/horarios` permite consultar:

- horario semanal de cada profesor
- clases asignadas
- horas libres
- guardias reales cubiertas

El horario fijo depende únicamente de:

- día de la semana
- hora

Las guardias reales sí dependen de fechas concretas.

---

# Modo test

La aplicación incorpora un sistema de simulación temporal.

Desde `config.py` pueden configurarse:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-04"
HORA_TEST = 1
```

Esto permite probar:

- horas pasadas
- recreos
- fuera de horario
- fechas futuras
- generación de guardias

sin depender de la hora real.

---

# Validaciones del sistema

El sistema protege tanto frontend como backend.

Ejemplos:

- no asignar guardias pasadas
- bloquear fuera de horario
- evitar duplicados
- impedir asignaciones inválidas
- impedir registro sin validación facial