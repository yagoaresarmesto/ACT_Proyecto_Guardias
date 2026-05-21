import os
import sys
import sqlite3
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
import modules.db.db_manager as db

from modules.guardias.motor import (
    generar_guardias,
    obtener_ranking_guardia,
)


SCHEMA_PATH = os.path.join(
    PROJECT_ROOT,
    "modules",
    "db",
    "schema.sql"
)


@pytest.fixture
def db_temporal(tmp_path, monkeypatch):
    db_path = tmp_path / "test_ies.db"

    monkeypatch.setattr(config, "DB_PATH", str(db_path))
    monkeypatch.setattr(db, "DB_PATH", str(db_path))

    conn = sqlite3.connect(db_path)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.close()

    return db_path


def preparar_datos_basicos():
    db.crear_profesor("Ana", "Matematicas")      # id 1
    db.crear_profesor("Luis", "Informatica")     # id 2
    db.crear_profesor("Marta", "Lengua")         # id 3

    # Ana tiene clase lunes 1ª hora
    db.crear_horario(
        id_profesor=1,
        dia_semana=1,
        hora=1,
        tipo="clase",
        aula="1ESO-A / Aula 101"
    )

    # Luis está libre lunes 1ª hora
    db.crear_horario(
        id_profesor=2,
        dia_semana=1,
        hora=1,
        tipo="libre",
        aula=None
    )

    # Marta tiene clase lunes 1ª hora
    db.crear_horario(
        id_profesor=3,
        dia_semana=1,
        hora=1,
        tipo="clase",
        aula="2ESO-B / Aula 202"
    )


def test_generar_guardia_si_profesor_con_clase_no_esta_presente(db_temporal):
    preparar_datos_basicos()

    fecha = "2026-05-04"
    dia_semana = 1

    # Solo están presentes Luis y Marta.
    # Ana tiene clase pero no está presente.
    db.registrar_evento(2, fecha, 1, "entrada")
    db.registrar_evento(3, fecha, 1, "entrada")

    generar_guardias(dia_semana, fecha)

    guardias = db.obtener_guardias(fecha)

    assert len(guardias) == 1
    assert guardias[0].id_profesor_ausente == 1
    assert guardias[0].aula == "1ESO-A / Aula 101"
    assert guardias[0].id_profesor_cubre is None


def test_no_genera_guardia_si_profesor_esta_presente(db_temporal):
    preparar_datos_basicos()

    fecha = "2026-05-04"
    dia_semana = 1

    db.registrar_evento(1, fecha, 1, "entrada")
    db.registrar_evento(2, fecha, 1, "entrada")
    db.registrar_evento(3, fecha, 1, "entrada")

    generar_guardias(dia_semana, fecha)

    guardias = db.obtener_guardias(fecha)

    assert len(guardias) == 0


def test_no_duplica_guardias_al_generar_varias_veces(db_temporal):
    preparar_datos_basicos()

    fecha = "2026-05-04"
    dia_semana = 1

    db.registrar_evento(2, fecha, 1, "entrada")
    db.registrar_evento(3, fecha, 1, "entrada")

    generar_guardias(dia_semana, fecha)
    generar_guardias(dia_semana, fecha)
    generar_guardias(dia_semana, fecha)

    guardias = db.obtener_guardias(fecha)

    assert len(guardias) == 1



def test_ranking_prioriza_profesor_disponible(db_temporal):
    preparar_datos_basicos()

    fecha = "2026-05-04"

    db.registrar_evento(1, fecha, 1, "entrada")
    db.registrar_evento(2, fecha, 1, "entrada")
    db.registrar_evento(3, fecha, 1, "entrada")

    ranking = obtener_ranking_guardia(
        dia_semana=1,
        fecha=fecha,
        hora=1,
        hora_actual=1
    )

    assert len(ranking) == 1
    assert ranking[0] == 2