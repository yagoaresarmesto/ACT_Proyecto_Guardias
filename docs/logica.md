# Lógica del sistema

## Detección de ausencias

El sistema compara:

- Horarios → profesores que deberían estar
- Presencia → profesores que han fichado

La diferencia entre ambos determina los profesores ausentes.

Ejemplo:

HORARIO = {1, 2, 3}  
PRESENCIA = {1, 3}  

Resultado: AUSENTES = {2}

---

## Motor de guardias (fase inicial)

El sistema comienza a generar guardias a partir de las ausencias detectadas.

### 1. Aulas sin profesor

Se detectan las aulas que quedan sin profesor cuando un docente con horario no está presente.

Ejemplo:

- Profesor 2 tiene clase en Aula 102 a la hora 2
- No ha registrado presencia

Resultado:
- Aula 102 necesita guardia

---

### 2. Profesores disponibles

Un profesor se considera disponible si:

- Está presente en el centro
- No tiene clase asignada en esa hora

Cálculo:

DISPONIBLES = PRESENTES - OCUPADOS

Ejemplo:

PRESENTES = {1, 3}  
OCUPADOS = {3}  

Resultado: DISPONIBLES = {1}

---

## Ejemplo completo de funcionamiento

Se ha probado el sistema con el siguiente escenario:

### Profesores
- Profesor 1
- Profesor 2
- Profesor 3

### Horarios
- Profesor 1 → Lunes, hora 1 → Aula 101
- Profesor 2 → Lunes, hora 2 → Aula 102
- Profesor 3 → Lunes, hora 2 → Aula 103

### Presencia
- Profesor 1 → presente
- Profesor 3 → presente
- Profesor 2 → ausente

---

### Resultado del sistema

#### 1. Ausencias detectadas
Profesores ausentes:

{2}

---

#### 2. Aulas sin profesor

[('Aula 102', 2)]

---

#### 3. Profesores disponibles

Profesores presentes:

{1, 3}

Profesores ocupados en hora 2:

{3}

Profesores disponibles:

{1}

---

#### 4. Ranking de profesores

[(1, 'Profesor 1', 0, 0)]

---

### Conclusión

El sistema identifica correctamente:

- Qué profesor está ausente
- Qué aula necesita cobertura
- Qué profesor puede cubrir la guardia

Este flujo constituye la base del motor de guardias.