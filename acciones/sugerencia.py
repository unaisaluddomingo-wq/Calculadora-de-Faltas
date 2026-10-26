import os
import random

from acciones.db_check import conectar

# La nota avisa al llegar al 75% del limite de faltas (con un limite del 20% son el 15% de las horas)
FRACCION_AVISO = 0.75


def _leer_porcentaje():
    with conectar() as con:
        fila = con.execute("SELECT valor FROM config WHERE clave = 'porcentaje_maximo'").fetchone()
    return int(fila[0]) if fila else None


def _porcentajes_por_asignatura():
    """Devuelve una lista (nombre, horas totales, horas faltadas) de cada asignatura."""
    with conectar() as con:
        filas = con.execute(
            """SELECT a.nombre, a.horas, COALESCE(SUM(f.horas), 0)
               FROM asignaturas a LEFT JOIN faltas f ON f.asignatura = a.nombre
               GROUP BY a.nombre, a.horas"""
        ).fetchall()
    return filas


def sugerencia():
    """Al iniciar el programa avisa de una asignatura (al azar si hay varias) cerca del limite de faltas,
    o felicita al usuario si no hay ninguna."""
    limite = _leer_porcentaje()
    if limite is None:
        return
    umbral = limite * FRACCION_AVISO
    # comparacion con enteros (faltadas/total >= limite*75%) para evitar errores de redondeo con decimales
    cerca = [nombre for nombre, total, faltadas in _porcentajes_por_asignatura() if faltadas * 400 >= limite * 3 * total]

    os.system("cls")
    if not cerca:
        print("NOTA: ¡Vas muy bien con tus faltas de asistencia! ¡Sigue asi!")
    else:
        print("NOTA: cuidado con {}, ¡tienes un {:g}% de faltas de asistencia o mas!".format(random.choice(cerca), umbral))
    input("Pulsa enter para continuar")
