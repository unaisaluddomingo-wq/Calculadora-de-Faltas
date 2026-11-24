"""Asignaturas desde la interfaz grafica: listarlas, crearlas, renombrarlas, cambiar sus horas y eliminarlas.
Cada funcion recibe los datos que envia la pagina y lanza ValueError con un mensaje para el usuario si no son validos."""
from acciones.db_check import conectar

MAX_HORAS = 800


def _entero(valor, minimo, maximo, mensaje):
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError(mensaje)
    texto = str(valor).strip()
    if not texto.isdecimal() or not minimo <= int(texto) <= maximo:
        raise ValueError(mensaje)
    return int(texto)


def _horas(valor):
    return _entero(valor, 1, MAX_HORAS, "Las horas tienen que ser un numero entre 1 y {}".format(MAX_HORAS))


def _nombre(valor, ignorar=None):
    """Devuelve el nombre limpio si no esta vacio, no es demasiado largo y no lo tiene otra asignatura."""
    nombre = valor.strip() if isinstance(valor, str) else ""
    if not 1 <= len(nombre) <= 60:
        raise ValueError("El nombre debe tener entre 1 y 60 caracteres")
    with conectar() as con:
        existentes = [fila[0] for fila in con.execute("SELECT nombre FROM asignaturas").fetchall()]
    for existente in existentes:
        if existente != ignorar and existente.lower() == nombre.lower():
            raise ValueError("Ya existe una asignatura llamada {}".format(existente))
    return nombre


def _existente(valor):
    """Devuelve el nombre tal y como esta guardado, o lanza ValueError si esa asignatura no existe."""
    with conectar() as con:
        fila = con.execute("SELECT nombre FROM asignaturas WHERE nombre = ?", (valor if isinstance(valor, str) else "",)).fetchone()
    if fila is None:
        raise ValueError("Esa asignatura ya no existe")
    return fila[0]


def listar():
    """Lista de asignaturas en el orden en que se crearon, como diccionarios {nombre, horas}."""
    with conectar() as con:
        filas = con.execute("SELECT nombre, horas FROM asignaturas ORDER BY rowid").fetchall()
    return [{"nombre": nombre, "horas": horas} for nombre, horas in filas]


def crear(datos):
    nombre = _nombre(datos.get("nombre"))
    horas = _horas(datos.get("horas"))
    with conectar() as con:
        con.execute("INSERT INTO asignaturas (nombre, horas) VALUES (?, ?)", (nombre, horas))


def renombrar(datos):
    """Cambia el nombre de la asignatura y tambien el de sus faltas ya registradas."""
    actual = _existente(datos.get("nombre"))
    nuevo = _nombre(datos.get("nuevo"), ignorar=actual)
    with conectar() as con:
        con.execute("UPDATE asignaturas SET nombre = ? WHERE nombre = ?", (nuevo, actual))
        con.execute("UPDATE faltas SET asignatura = ? WHERE asignatura = ?", (nuevo, actual))


def cambiar_horas(datos):
    nombre = _existente(datos.get("nombre"))
    horas = _horas(datos.get("horas"))
    with conectar() as con:
        con.execute("UPDATE asignaturas SET horas = ? WHERE nombre = ?", (horas, nombre))


def eliminar(datos):
    """Borra la asignatura y sus faltas. No deja borrar la ultima que queda."""
    nombre = _existente(datos.get("nombre"))
    with conectar() as con:
        if con.execute("SELECT COUNT(*) FROM asignaturas").fetchone()[0] <= 1:
            raise ValueError("No puedes eliminar la unica asignatura que hay")
        con.execute("DELETE FROM faltas WHERE asignatura = ?", (nombre,))
        con.execute("DELETE FROM asignaturas WHERE nombre = ?", (nombre,))
