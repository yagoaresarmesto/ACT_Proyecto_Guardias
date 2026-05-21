import os
import sys
import sqlite3
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
import modules.db.db_manager as db
import modules.presencia.registro as registro


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


def test_primer_registro_crea_referencia_facial(db_temporal, monkeypatch):
    db.crear_profesor("Ana", "Matematicas")

    monkeypatch.setattr(
        registro,
        "registrar_referencias_profesor",
        lambda profesor_id: "static/faces/profesor_1/encodings.pkl"
    )

    resultado = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    profesor = db.obtener_profesor_por_id(1)

    assert resultado is False
    assert profesor.rfid_uid == "static/faces/profesor_1/encodings.pkl"
    assert db.obtener_eventos("2026-05-04") == []


def test_verificacion_correcta_registra_entrada(db_temporal, monkeypatch):
    db.crear_profesor("Luis", "Informatica")

    db.actualizar_rfid_uid_profesor(
        1,
        "static/faces/profesor_1/encodings.pkl"
    )

    monkeypatch.setattr(
        registro,
        "verificar_profesor_en_vivo",
        lambda ruta: True
    )

    resultado = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    eventos = db.obtener_eventos("2026-05-04")

    assert resultado is True
    assert len(eventos) == 1
    assert eventos[0]["tipo"] == "entrada"
    assert eventos[0]["hora"] == 1


def test_verificacion_correcta_registra_salida(db_temporal, monkeypatch):
    db.crear_profesor("Marta", "Lengua")

    db.actualizar_rfid_uid_profesor(
        1,
        "static/faces/profesor_1/encodings.pkl"
    )

    monkeypatch.setattr(
        registro,
        "verificar_profesor_en_vivo",
        lambda ruta: True
    )

    registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    resultado = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=2
    )

    eventos = db.obtener_eventos("2026-05-04")

    assert resultado is True
    assert len(eventos) == 2
    assert eventos[1]["tipo"] == "salida"
    assert eventos[1]["hora"] == 2


def test_verificacion_fallida_no_registra_evento(db_temporal, monkeypatch):
    db.crear_profesor("Carlos", "Historia")

    db.actualizar_rfid_uid_profesor(
        1,
        "static/faces/profesor_1/encodings.pkl"
    )

    monkeypatch.setattr(
        registro,
        "verificar_profesor_en_vivo",
        lambda ruta: False
    )

    resultado = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    eventos = db.obtener_eventos("2026-05-04")

    assert resultado is False
    assert len(eventos) == 0


def test_no_permite_dos_eventos_en_la_misma_hora(db_temporal, monkeypatch):
    db.crear_profesor("Elena", "Fisica")

    db.actualizar_rfid_uid_profesor(
        1,
        "static/faces/profesor_1/encodings.pkl"
    )

    monkeypatch.setattr(
        registro,
        "verificar_profesor_en_vivo",
        lambda ruta: True
    )

    primero = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    segundo = registro.registrar_evento(
        profesor_id=1,
        fecha="2026-05-04",
        hora=1
    )

    eventos = db.obtener_eventos("2026-05-04")

    assert primero is True
    assert segundo is False
    assert len(eventos) == 1