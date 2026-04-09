from db.db_manager import obtener_horarios, obtener_presencia

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