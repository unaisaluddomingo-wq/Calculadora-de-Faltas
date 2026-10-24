from acciones.db_check import conectar
from acciones.elegir_asignatura import elegir_asignatura
from acciones.pedir_fecha import pedir_fecha


def añadir():
    nombre = elegir_asignatura("Elige la asignatura a la que has faltado: ")
    total_horas = int(input("¿Cuantas horas has faltado?: "))
    fecha = pedir_fecha()
    justificada = input("¿Es justificada? (S/N): ").strip().upper() == "S"

    with conectar() as con:
        con.execute(
            "INSERT INTO faltas (asignatura, fecha, justificada, horas) VALUES (?, ?, ?, ?)",
            (nombre, fecha, int(justificada), total_horas),
        )
    print("Falta de asistencia registrada")
    input("Pulsa enter para continuar")
