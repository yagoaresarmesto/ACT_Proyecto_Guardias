from datetime import datetime, time


def obtener_hora_lectiva_actual():
    ahora = datetime.now().time()

    tramos = [
        (time(8, 50), time(9, 40), 1),
        (time(9, 40), time(10, 30), 2),
        (time(10, 30), time(11, 20), 3),

        (time(11, 20), time(11, 40), None),  # recreo (actualmente lo estoy contando como fuera de horario)

        (time(11, 40), time(12, 30), 4),
        (time(12, 30), time(13, 20), 5),
        (time(13, 20), time(14, 10), 6),

        (time(16, 0), time(17, 0), 7),
        (time(17, 0), time(18, 0), 8),
        (time(18, 0), time(19, 0), 9),
        (time(19, 0), time(20, 0), 10),
    ]

    for inicio, fin, hora in tramos:
        if inicio <= ahora < fin:
            return hora

    return None