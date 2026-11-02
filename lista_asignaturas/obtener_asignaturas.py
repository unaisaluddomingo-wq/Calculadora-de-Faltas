"""Las asignaturas (con el total de horas de cada una) las define el usuario y se guardan en la base de datos. Es
importante saber exactamente cuantas horas dura cada asignatura ya que las faltas no se cuentan globalmente, sino
individualmente"""
from acciones.db_check import conectar


def asignaturas():
    """Devuelve un diccionario nombre -> total de horas, en el orden en que se crearon."""
    with conectar() as con:
        filas = con.execute("SELECT nombre, horas FROM asignaturas ORDER BY rowid").fetchall()
    return dict(filas)
