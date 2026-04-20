class Profesor:
    def __init__(self, id_profesor, nombre, departamento, rfid_uid=None,
                 guardias_semana=0, guardias_acumuladas=0):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.departamento = departamento
        self.rfid_uid = rfid_uid
        self.guardias_semana = guardias_semana
        self.guardias_acumuladas = guardias_acumuladas


class Horario:
    def __init__(self, id_horario, id_profesor, dia_semana, hora, tipo, aula):
        self.id_horario = id_horario
        self.id_profesor = id_profesor
        self.dia_semana = dia_semana
        self.hora = hora
        self.tipo = tipo
        self.aula = aula


class Presencia:
    def __init__(self, id_presencia, id_profesor, fecha, hora, presente):
        self.id_presencia = id_presencia
        self.id_profesor = id_profesor
        self.fecha = fecha
        self.hora = hora
        self.presente = bool(presente)
