# Lógica del sistema

## Detección de ausencias

El sistema compara:

- Horarios → profesores que deberían estar
- Presencia → profesores que han fichado

La diferencia entre ambos determina los profesores ausentes.

Ejemplo:

HORARIO = {1, 2}  
PRESENCIA = {1}  

Resultado: AUSENTES = {2}

## Motor de guardias (fase inicial)

El sistema comienza a generar guardias a partir de las ausencias detectadas.

### 1. Aulas sin profesor

Se detectan las aulas que quedan sin profesor cuando un docente con horario no está presente.

Ejemplo:

- Profesor 2 tiene clase en Aula 239 a la hora 2
- No ha registrado presencia

Resultado:
- Aula 239 necesita guardia

---

### 2. Profesores disponibles

Un profesor se considera disponible si:

- Está presente en el centro
- No tiene clase asignada en esa hora

Cálculo:

DISPONIBLES = PRESENTES - OCUPADOS

Ejemplo:

PRESENTES = {1, 2}  
OCUPADOS = {2}  

Resultado: DISPONIBLES = {1}

