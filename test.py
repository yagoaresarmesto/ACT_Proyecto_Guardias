from db.db_manager import crear_profesor, obtener_profesores, crear_horario, obtener_horarios, registrar_entrada, obtener_presencia

#Para probar diferentes funciones de la db sqlite
'''
crear_profesor("Yago Ares Armesto")
crear_profesor("Jesus Ares Armesto")

print(obtener_profesores())
'''

'''
crear_horario(1, "Lunes", 1, "Aula 238")
crear_horario(2, "Lunes", 2, "Aula 239")

print(obtener_horarios())

'''

'''
registrar_entrada(1, "2026-04-09", "08:00")
registrar_entrada(2, "2026-04-09", "08:05")
'''

print(obtener_presencia())