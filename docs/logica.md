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