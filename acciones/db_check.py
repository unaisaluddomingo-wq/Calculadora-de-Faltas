"""Conexion con la base de datos (SQLite). Si no existe se crea. Las consultas de cada accion estan en el fichero
de la propia accion, que usa conectar() para acceder a la base de datos."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "faltas.db"


@contextmanager
def conectar():
    """Abre una conexion a la base de datos: guarda los cambios al salir del with y siempre cierra la conexion."""
    con = sqlite3.connect(DB_PATH)
    try:
        with con:
            yield con
    finally:
        con.close()


def comprobar_db():
    """Crea la base de datos y la tabla si no existen. Si ya existen, no toca nada."""
    with conectar() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS faltas (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   asignatura TEXT NOT NULL,
                   fecha TEXT NOT NULL,
                   justificada INTEGER NOT NULL CHECK (justificada IN (0, 1)),
                   horas INTEGER NOT NULL CHECK (horas > 0)
               )"""
        )
