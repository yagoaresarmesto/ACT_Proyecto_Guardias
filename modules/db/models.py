class Profesor:
    def __init__(self, id_profesor, nombre, departamento=None,
                 rfid_uid=None,
                 guardias_semana=0, guardias_acumuladas=0):

        self.id_profesor = id_profesor
        self.nombre = nombre
        self.departamento = departamento
        self.rfid_uid = rfid_uid
        self.guardias_semana = guardias_semana
        self.guardias_acumuladas = guardias_acumuladas

class Guardia:
    def __init__(self, id_guardia, fecha, hora, aula,
                 id_profesor_ausente,
                 id_profesor_cubre=None,
                 ausente_nombre=None,
                 cubre_nombre=None):

        self.id_guardia = id_guardia
        self.fecha = fecha
        self.hora = hora
        self.aula = aula

        self.id_profesor_ausente = id_profesor_ausente
        self.id_profesor_cubre = id_profesor_cubre

        self.ausente_nombre = ausente_nombre
        self.cubre_nombre = cubre_nombre