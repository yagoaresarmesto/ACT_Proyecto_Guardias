from db.db_manager import obtener_horarios, obtener_presencia
from modules.guardias.reglas import ordenar_por_guardias

def obtener_aulas_sin_profesor(dia, fecha):
    # Obtener datos desde db_manager
    horarios = obtener_horarios()
    presencia = obtener_presencia()

    # Profesores presentes
    profesores_presentes = {p[1] for p in presencia if p[2] == fecha}

    aulas_sin_profesor = []

    for horario in horarios:
        _, profesor_id, dia_h, hora, aula = horario

        if dia_h == dia and profesor_id not in profesores_presentes:
            aulas_sin_profesor.append((aula, hora))

    return aulas_sin_profesor

def obtener_profesores_disponibles(dia, hora, fecha):
    horarios = obtener_horarios()
    presencia = obtener_presencia()

    # Profesores presentes
    profesores_presentes = {p[1] for p in presencia if p[2] == fecha}

    # Profesores ocupados en esa hora
    profesores_ocupados = {
        h[1] for h in horarios if h[2] == dia and h[3] == hora
    }

    # Disponibles = presentes - ocupados
    disponibles = profesores_presentes - profesores_ocupados

    return disponibles

#Asignar guardias
def asignar_guardias(dia, fecha):
    aulas = obtener_aulas_sin_profesor(dia, fecha)

    resultado = []
    profesores_usados = set()

    for aula, hora in aulas:
        disponibles = obtener_profesores_disponibles(dia, hora, fecha)

        disponibles = disponibles - profesores_usados

        if not disponibles:
            resultado.append((aula, hora, None))
            continue

        ranking = ordenar_por_guardias(disponibles)

        profesor_asignado = ranking[0]

        resultado.append((aula, hora, profesor_asignado))

        profesores_usados.add(profesor_asignado[0])

    return resultado