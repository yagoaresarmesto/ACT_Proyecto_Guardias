# Arquitectura del sistema

El sistema sigue una arquitectura modular separando responsabilidades:

- app.py → rutas Flask
- db_manager → acceso a base de datos
- guardias/motor.py → lógica de cálculo de guardias
- guardias/reglas.py → reglas de prioridad (pendiente)

Flujo actual:

Flask → motor → db_manager → SQLite