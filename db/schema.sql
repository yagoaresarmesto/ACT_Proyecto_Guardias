CREATE TABLE profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    guardias_acumuladas INTEGER DEFAULT 0,
    guardias_semana INTEGER DEFAULT 0
);

CREATE TABLE horarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER,
    dia TEXT,
    hora INTEGER,
    aula TEXT,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE presencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER,
    fecha TEXT,
    hora_entrada TEXT,
    hora_salida TEXT,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE ausencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER,
    fecha TEXT,
    hora INTEGER,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE guardias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER,
    aula TEXT,
    hora INTEGER,
    fecha TEXT,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);