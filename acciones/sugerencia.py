import os
import random

from acciones.db_check import conectar

# Avisos segun el porcentaje del limite de faltas ya consumido (con un limite del 20%, el aviso es al 10% de las
# horas y la alerta al 16%)
PORCENTAJE_AVISO = 50
PORCENTAJE_ALERTA = 80


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
    """Al iniciar el programa avisa de una asignatura (al azar si hay varias) que llega al 80% o al 50% del limite
    de faltas (muestra el aviso mas grave que se cumpla), o felicita al usuario si no hay ninguna."""
    limite = _leer_porcentaje()
    if limite is None:
        return
    filas = _porcentajes_por_asignatura()

    def en_umbral(porcentaje):
        # comparacion con enteros (faltadas/total >= limite% * porcentaje%) para evitar errores de redondeo
        return [nombre for nombre, total, faltadas in filas if faltadas * 10000 >= limite * porcentaje * total]

    alerta = en_umbral(PORCENTAJE_ALERTA)
    aviso = en_umbral(PORCENTAJE_AVISO)

    os.system("cls")
    if alerta:
        print("ALERTA: cuidado con {}, ¡tienes un {:g}% de faltas de asistencia o mas!".format(
            random.choice(alerta), limite * PORCENTAJE_ALERTA / 100))
    elif aviso:
        print("AVISO: ojo con {}, ¡ya tienes un {:g}% de faltas de asistencia o mas!".format(
            random.choice(aviso), limite * PORCENTAJE_AVISO / 100))
    else:
        print("NOTA: ¡Vas muy bien con tus faltas de asistencia! ¡Sigue asi!")
    input("Pulsa enter para continuar")
