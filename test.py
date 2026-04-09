from db.db_manager import crear_profesor, obtener_profesores, crear_horario, obtener_horarios

'''
crear_profesor("Yago Ares Armesto")
crear_profesor("Jesus Ares Armesto")

print(obtener_profesores())
'''

crear_horario(1, "Lunes", 1, "Aula 238")
crear_horario(2, "Lunes", 2, "Aula 239")

print(obtener_horarios())