PRAGMA foreign_keys = ON;

CREATE TABLE profesores (
    id_profesor     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    departamento    TEXT,
    rfid_uid        TEXT,      -- opcional: identificación hardware
    guardias_semana INTEGER DEFAULT 0,
    guardias_acumuladas INTEGER DEFAULT 0
);


CREATE TABLE horario (
    id_horario   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor  INTEGER NOT NULL,
    dia_semana   INTEGER NOT NULL CHECK(dia_semana BETWEEN 1 AND 5),
    hora         INTEGER NOT NULL CHECK(hora BETWEEN 1 AND 10),
    tipo         TEXT NOT NULL CHECK(tipo IN ('clase','guardia','libre')),
    aula         TEXT,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE presencia (
    id_presencia  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor   INTEGER NOT NULL,
    fecha         DATE NOT NULL,
    hora          INTEGER NOT NULL,
    presente      BOOLEAN NOT NULL CHECK(presente IN (0,1)),
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE ausencias (
    id_ausencia   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor   INTEGER NOT NULL,
    fecha         DATE NOT NULL,
    hora          INTEGER NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE guardias (
    id_guardia            INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha                 DATE NOT NULL,
    hora                  INTEGER NOT NULL,
    aula                  TEXT NOT NULL,
    id_profesor_ausente   INTEGER NOT NULL,
    id_profesor_cubre     INTEGER,
    FOREIGN KEY (id_profesor_ausente) REFERENCES profesores(id_profesor)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_profesor_cubre) REFERENCES profesores(id_profesor)
        ON DELETE SET NULL ON UPDATE CASCADE
);
