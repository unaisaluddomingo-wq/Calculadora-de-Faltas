"""Faltas de asistencia desde la interfaz grafica: listarlas, añadirlas, modificarlas y borrarlas.
Cada funcion recibe los datos que envia la pagina y lanza ValueError con un mensaje para el usuario si no son validos."""
import re
from datetime import date

from acciones.db_check import conectar


def _entero(valor, minimo, maximo, mensaje):
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError(mensaje)
    texto = str(valor).strip()
    if not texto.isdecimal() or not minimo <= int(texto) <= maximo:
        raise ValueError(mensaje)
    return int(texto)


def _asignatura(valor):
    """Devuelve el nombre tal y como esta guardado, o lanza ValueError si esa asignatura no existe."""
    with conectar() as con:
        fila = con.execute("SELECT nombre FROM asignaturas WHERE nombre = ?", (valor if isinstance(valor, str) else "",)).fetchone()
    if fila is None:
        raise ValueError("Esa asignatura no existe")
    return fila[0]


def _fecha(valor):
    """Comprueba que la fecha tiene el formato AAAA-MM-DD, existe y no es futura."""
    if not isinstance(valor, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor):
        raise ValueError("Elige la fecha de la falta")
    try:
        fecha = date.fromisoformat(valor)
    except ValueError:
        raise ValueError("Esa fecha no existe")
    if fecha > date.today():
        raise ValueError("La fecha no puede ser futura")
    return fecha.isoformat()


def _justificada(valor):
    if valor in (True, 1, "1", "S", "s"):
        return 1
    if valor in (False, 0, "0", "N", "n"):
        return 0
    raise ValueError("Indica si la falta es justificada o no")


def _datos_falta(datos):
    return (
        _asignatura(datos.get("asignatura")),
        _fecha(datos.get("fecha")),
        _justificada(datos.get("justificada")),
        _entero(datos.get("horas"), 1, 24, "Las horas faltadas tienen que ser un numero entre 1 y 24"),
    )


def _id(datos):
    id_falta = _entero(datos.get("id"), 1, 10 ** 9, "Esa falta no existe")
    with conectar() as con:
        if con.execute("SELECT 1 FROM faltas WHERE id = ?", (id_falta,)).fetchone() is None:
            raise ValueError("Esa falta ya no existe")
    return id_falta


def listar():
    """Lista de faltas como diccionarios {id, asignatura, fecha, horas, justificada}."""
    with conectar() as con:
        filas = con.execute("SELECT id, asignatura, fecha, horas, justificada FROM faltas ORDER BY id").fetchall()
    return [{"id": id_falta, "asignatura": asignatura, "fecha": fecha, "horas": horas, "justificada": justificada}
            for id_falta, asignatura, fecha, horas, justificada in filas]


def añadir(datos):
    with conectar() as con:
        con.execute("INSERT INTO faltas (asignatura, fecha, justificada, horas) VALUES (?, ?, ?, ?)", _datos_falta(datos))


def modificar(datos):
    """Sustituye todos los campos de la falta (menos el id) por los que llegan del formulario."""
    id_falta = _id(datos)
    with conectar() as con:
        con.execute("UPDATE faltas SET asignatura = ?, fecha = ?, justificada = ?, horas = ? WHERE id = ?",
                    _datos_falta(datos) + (id_falta,))


def borrar(datos):
    id_falta = _id(datos)
    with conectar() as con:
        con.execute("DELETE FROM faltas WHERE id = ?", (id_falta,))
