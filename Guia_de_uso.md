# Guía rápida de uso

## 1. Inicializar la base de datos

Desde la raíz del proyecto:

```bash
python -m modules.db.init_db
```

Esto crea de nuevo la base de datos SQLite usando el esquema definido en:

```text
modules/db/schema.sql
```

---

## 2. Cargar datos de prueba

Después de inicializar la base de datos:

```bash
python cargar_datos.py
```

Este script carga datos demo:

- profesores
- horarios
- presencias
- ausencias
- guardias
- guardias ya asignadas
- rankings

---

## 3. Configurar modo demo

En `config.py`, para probar el escenario preparado, usar:

```python
MODO_TEST = True
FECHA_TEST = "2026-05-28"
HORA_TEST = 3
```

Con esta configuración se pueden ver:

- guardias de horas pasadas
- guardias actuales
- guardias futuras
- guardias pendientes
- guardias cubiertas
- bloqueo de asignaciones no permitidas

---

## 4. Ejecutar la aplicación

```bash
python app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

---

## 5. Flujo recomendado para probar

1. Entrar en `/presencia`
2. Revisar profesores presentes y ausentes
3. Entrar en `/guardias`
4. Comprobar guardias generadas para `2026-05-28`
5. Revisar guardias pasadas, pendientes y asignadas
6. Entrar en `/horarios`
7. Seleccionar profesores distintos para ver horarios y guardias reales

---

## 6. Volver a modo real

Cuando se quiera usar la fecha y hora real del sistema:

```python
MODO_TEST = False
FECHA_TEST = None
HORA_TEST = None
```