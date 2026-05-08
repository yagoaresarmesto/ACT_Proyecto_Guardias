# Arquitectura del sistema

El proyecto sigue una arquitectura modular basada en separación de responsabilidades.

Cada módulo se encarga de una parte concreta del sistema, facilitando:

- mantenimiento
- escalabilidad
- testing
- reutilización de código

---

# Arquitectura general

El sistema se divide en varias capas:

```text
Flask (interfaz web)
        ↓
Servicios y lógica de negocio
        ↓
Acceso a datos (SQLite)
```

---

# Estructura del proyecto

```text
project/
│
├── app.py
│
├── modules/
│   ├── db/
│   ├── guardias/
│   ├── presencia/
│   ├── horarios/
│   └── utils/
│
├── templates/
├── static/
│
├── test2.py
└── requirements.txt
```

---

# app.py

Archivo principal de Flask.

Se encarga de:

- Definir rutas web
- Coordinar los módulos
- Gestionar el modo test
- Renderizar las vistas HTML

Principales rutas:

| Ruta | Función |
|---|---|
| `/` | Página principal |
| `/presencia` | Gestión de presencia |
| `/guardias` | Gestión de guardias |
| `/horarios` | Consulta de horarios |

---

# Módulo db

Ruta:

```text
modules/db/
```

Responsabilidad:

- Acceso a base de datos SQLite
- Consultas SQL
- Transformación de filas en objetos Python

Archivo principal:

```text
db_manager.py
```

Funciones típicas:

- crear profesores
- registrar presencia
- obtener horarios
- generar guardias
- asignar coberturas

---

# Módulo guardias

Ruta:

```text
modules/guardias/
```

Responsabilidad:

- Detectar ausencias
- Generar guardias
- Obtener profesores disponibles
- Aplicar ranking de prioridad

Archivos:

| Archivo | Función |
|---|---|
| `motor.py` | Lógica principal |
| `reglas.py` | Ordenación y ranking |
| `models.py` | Clases de dominio |

---

# Módulo presencia

Ruta:

```text
modules/presencia/
```

Responsabilidad:

- Registrar entradas y salidas
- Consultar presencia actual
- Determinar profesores presentes

Archivo principal:

```text
registro.py
```

---

# Módulo horarios

Ruta:

```text
modules/horarios/
```

Responsabilidad:

- Construcción de horarios semanales
- Mezcla de horario fijo y guardias reales
- Generación de tablas para la interfaz

Archivo principal:

```text
servicio.py
```

---

# Módulo utils

Ruta:

```text
modules/utils/
```

Responsabilidad:

- Funciones auxiliares
- Gestión de tiempo y horas lectivas
- Utilidades comunes

---

# Base de datos

El sistema utiliza SQLite como motor de persistencia.

Ventajas:

- Ligero
- Fácil de desplegar
- Sin servidor externo
- Ideal para prototipos y proyectos académicos

---

# Interfaz web

La interfaz se desarrolla utilizando:

- Flask
- Jinja2
- HTML
- CSS

La aplicación utiliza renderizado server-side mediante plantillas.

---

# Modo test

La aplicación incorpora un sistema de testing integrado.

Desde `app.py` se pueden simular:

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

sin depender de la hora real del sistema.

---

# Flujo principal del sistema

## 1. Horario

El sistema consulta el horario semanal planificado.

---

## 2. Presencia

Se obtiene la presencia real registrada.

---

## 3. Ausencias

Se detectan profesores con clase que no están presentes.

---

## 4. Guardias

Se generan guardias automáticamente.

---

## 5. Ranking

Se calculan profesores disponibles y se ordenan por prioridad.

---

## 6. Asignación

El usuario asigna manualmente la cobertura desde la interfaz web.

---

# Decisiones de diseño

## Separación entre planificación y realidad

El sistema diferencia claramente entre:

- horario teórico
- presencia real
- incidencias
- coberturas

---

## Arquitectura modular

Cada responsabilidad se encuentra aislada en un módulo específico.

Esto evita mezclar:

- lógica de negocio
- acceso a datos
- interfaz

---

## Protección backend + frontend

Las restricciones importantes se validan tanto:

- visualmente en la interfaz
- como internamente en Flask

Ejemplo:

- bloqueo de guardias pasadas
- bloqueo fuera de horario

---

# Estado actual

Actualmente el sistema es completamente funcional a nivel software.

El siguiente paso del proyecto consiste en integrar hardware externo para automatizar el registro de presencia mediante Pi Camera.