import os
import sys
import sqlite3
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
import modules.db.db_manager as db


SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
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


def test_crear_y_obtener_profesor(db_temporal):
    db.crear_profesor("Ana", "Matematicas")

    profesores = db.obtener_profesores()

    assert len(profesores) == 1
    assert profesores[0].nombre == "Ana"
    assert profesores[0].departamento == "Matematicas"


def test_obtener_profesor_por_id_y_actualizar_rfid(db_temporal):
    db.crear_profesor("Luis", "Informatica")

    profesor = db.obtener_profesor_por_id(1)

    assert profesor is not None
    assert profesor.nombre == "Luis"
    assert profesor.rfid_uid is None

    db.actualizar_rfid_uid_profesor(1, "static/faces/profesor_1/encodings.pkl")

    profesor_actualizado = db.obtener_profesor_por_id(1)

    assert profesor_actualizado.rfid_uid == "static/faces/profesor_1/encodings.pkl"


def test_registrar_eventos_y_obtener_presentes(db_temporal):
    db.crear_profesor("Marta", "Lengua")

    fecha = "2026-05-04"

    db.registrar_evento(1, fecha, 1, "entrada")

    presentes = db.obtener_presentes(fecha)

    assert 1 in presentes

    db.registrar_evento(1, fecha, 2, "salida")

    presentes = db.obtener_presentes(fecha)

    assert 1 not in presentes


def test_crear_horario_y_filtrar_por_dia(db_temporal):
    db.crear_profesor("Carlos", "Historia")

    db.crear_horario(
        id_profesor=1,
        dia_semana=1,
        hora=1,
        tipo="clase",
        aula="1ESO-A / Aula 101"
    )

    db.crear_horario(
        id_profesor=1,
        dia_semana=2,
        hora=2,
        tipo="libre",
        aula=None
    )

    horario_lunes = db.obtener_horario_por_dia(1)

    assert len(horario_lunes) == 1
    assert horario_lunes[0]["tipo"] == "clase"
    assert horario_lunes[0]["aula"] == "1ESO-A / Aula 101"


def test_crear_y_asignar_guardia(db_temporal):
    db.crear_profesor("Ana", "Matematicas")
    db.crear_profesor("Luis", "Informatica")

    fecha = "2026-05-04"

    db.crear_guardia(
        fecha=fecha,
        hora=1,
        aula="Aula 101",
        id_profesor_ausente=1
    )

    guardias = db.obtener_guardias(fecha)

    assert len(guardias) == 1
    assert guardias[0].ausente_nombre == "Ana"
    assert guardias[0].id_profesor_cubre is None

    db.asignar_guardia(guardias[0].id_guardia, 2)

    guardias_actualizadas = db.obtener_guardias(fecha)

    assert guardias_actualizadas[0].id_profesor_cubre == 2
    assert guardias_actualizadas[0].cubre_nombre == "Luis"


def test_existe_guardia_y_profesores_asignados(db_temporal):
    db.crear_profesor("Ana", "Matematicas")
    db.crear_profesor("Luis", "Informatica")

    fecha = "2026-05-04"

    db.crear_guardia(fecha, 1, "Aula 101", 1)

    assert db.existe_guardia(fecha, 1, "Aula 101") is True
    assert db.existe_guardia(fecha, 2, "Aula 999") is False

    guardia = db.obtener_guardias(fecha)[0]

    db.asignar_guardia(guardia.id_guardia, 2)

    asignados = db.obtener_profesores_asignados(fecha, 1)

    assert asignados == {2}


def test_sumar_guardia_actualiza_contadores(db_temporal):
    db.crear_profesor("Elena", "Fisica")

    profesor = db.obtener_profesor_por_id(1)

    assert profesor.guardias_semana == 0
    assert profesor.guardias_acumuladas == 0

    db.sumar_guardia(1)

    profesor_actualizado = db.obtener_profesor_por_id(1)

    assert profesor_actualizado.guardias_semana == 1
    assert profesor_actualizado.guardias_acumuladas == 1