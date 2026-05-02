class ProfesorDisponible:
    def __init__(self, id_profesor, guardias_acumuladas, guardias_semana, carga_lectiva):
        self.id_profesor = id_profesor
        self.guardias_acumuladas = guardias_acumuladas
        self.guardias_semana = guardias_semana
        self.carga_lectiva = carga_lectiva


class Guardia:
    def __init__(self, hora, aula, id_profesor_ausente):
        self.hora = hora
        self.aula = aula
        self.id_profesor_ausente = id_profesor_ausente