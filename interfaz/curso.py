"""Datos del curso desde la interfaz grafica: el porcentaje maximo de faltas, la configuracion inicial (porcentaje y
primeras asignaturas) y terminar el año escolar (borrar la base de datos)."""
import os

from acciones.db_check import DB_PATH, conectar

MAX_HORAS = 800


def _entero(valor, minimo, maximo, mensaje):
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError(mensaje)
    texto = str(valor).strip()
    if not texto.isdecimal() or not minimo <= int(texto) <= maximo:
        raise ValueError(mensaje)
    return int(texto)


def _porcentaje(valor):
    return _entero(valor, 1, 100, "El porcentaje tiene que ser un numero entre 1 y 100")


def leer_limite():
    """Porcentaje maximo de horas que se puede faltar en cada asignatura, o None si aun no se ha elegido."""
    with conectar() as con:
        fila = con.execute("SELECT valor FROM config WHERE clave = 'porcentaje_maximo'").fetchone()
    return int(fila[0]) if fila else None


def cambiar_limite(datos):
    porcentaje = _porcentaje(datos.get("porcentaje"))
    with conectar() as con:
        con.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES ('porcentaje_maximo', ?)", (str(porcentaje),))


def configurar(datos):
    """Primer inicio: guarda el porcentaje y las asignaturas que ha escrito el usuario (al menos una)."""
    porcentaje = _porcentaje(datos.get("porcentaje"))
    lista = datos.get("asignaturas")
    if not isinstance(lista, list) or not lista:
        raise ValueError("Añade al menos una asignatura")

    with conectar() as con:
        vistos = [fila[0].lower() for fila in con.execute("SELECT nombre FROM asignaturas").fetchall()]
    nuevas = []
    for asignatura in lista:
        if not isinstance(asignatura, dict):
            raise ValueError("Datos de asignatura incorrectos")
        nombre = asignatura.get("nombre").strip() if isinstance(asignatura.get("nombre"), str) else ""
        if not 1 <= len(nombre) <= 60:
            raise ValueError("El nombre debe tener entre 1 y 60 caracteres")
        if nombre.lower() in vistos:
            raise ValueError("Ya existe una asignatura llamada {}".format(nombre))
        vistos.append(nombre.lower())
        horas = _entero(asignatura.get("horas"), 1, MAX_HORAS,
                        "Las horas tienen que ser un numero entre 1 y {}".format(MAX_HORAS))
        nuevas.append((nombre, horas))

    with conectar() as con:
        con.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES ('porcentaje_maximo', ?)", (str(porcentaje),))
        con.executemany("INSERT INTO asignaturas (nombre, horas) VALUES (?, ?)", nuevas)


def terminar_año():
    """Borra la base de datos entera. Al volver a abrir la app empieza la configuracion desde cero."""
    if DB_PATH.exists():
        os.remove(DB_PATH)
