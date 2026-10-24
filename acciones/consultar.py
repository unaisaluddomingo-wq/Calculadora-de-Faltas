from asignaturas import asignaturas
from acciones.db_check import conectar
from acciones.elegir_asignatura import elegir_asignatura


def _horas_faltadas(asignatura=None):
    """Total de horas faltadas en una asignatura, o en total si asignatura es None."""
    with conectar() as con:
        if asignatura is None:
            fila = con.execute("SELECT COALESCE(SUM(horas), 0) FROM faltas").fetchone()
        else:
            fila = con.execute(
                "SELECT COALESCE(SUM(horas), 0) FROM faltas WHERE asignatura = ?",
                (asignatura,),
            ).fetchone()
    return fila[0]


def consultar():
    ASIGNATURAS = asignaturas()
    opcion = input("1. Ver faltas totales\n2. Ver faltas de una asignatura\nElige una opcion: ").strip()

    if opcion == "1":
        print("Faltas totales: {}/{}".format(_horas_faltadas(), sum(ASIGNATURAS.values())))
    elif opcion == "2":
        nombre = elegir_asignatura("Introduce que asignatura quieres consultar: ")
        print("{}: {}/{}".format(nombre, _horas_faltadas(nombre), ASIGNATURAS[nombre]))
    else:
        print("Opcion incorrecta")

    input("Pulsa enter para continuar")
