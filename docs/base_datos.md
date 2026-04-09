# Base de Datos

Se utiliza SQLite como sistema de almacenamiento.

## Tablas principales

### profesores
- id
- nombre
- guardias_acumuladas
- guardias_semana

### horarios
- profesor_id
- dia
- hora
- aula

### presencia
- profesor_id
- fecha
- hora_entrada
- hora_salida

### ausencias
- profesor_id
- fecha
- hora

### guardias
- profesor_id
- aula
- hora
- fecha