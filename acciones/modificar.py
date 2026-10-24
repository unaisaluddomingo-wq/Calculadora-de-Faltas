from acciones.db_check import conectar
from acciones.elegir_asignatura import elegir_asignatura
from acciones.pedir_fecha import pedir_fecha


def _actualizar(id_falta, campo, valor):
    # campo siempre viene de las opciones fijas de modificar(), nunca del usuario
    with conectar() as con:
        con.execute("UPDATE faltas SET {} = ? WHERE id = ?".format(campo), (valor, id_falta))


def modificar():
    with conectar() as con:
        faltas = con.execute("SELECT id, asignatura, fecha, justificada, horas FROM faltas ORDER BY id").fetchall()
    if not faltas:
        print("No hay faltas registradas")
        input("Pulsa enter para continuar")
        return

    for id_falta, asignatura, fecha, justificada, horas in faltas:
        print("{}. {} - {} - {}h - {}".format(id_falta, asignatura, fecha, horas, "S" if justificada else "N"))
    id_falta = int(input("Elige la falta de asistencia que deseas modificar (id): "))
    if id_falta not in [falta[0] for falta in faltas]:
        print("Esa falta no existe")
        input("Pulsa enter para continuar")
        return

    accion = input("1. Modificar\n2. Borrar\nElige una opcion: ").strip()
    if accion == "2":
        if input("¿Seguro que quieres borrarla? (S/N): ").strip().upper() == "S":
            with conectar() as con:
                con.execute("DELETE FROM faltas WHERE id = ?", (id_falta,))
            print("Falta borrada")
    elif accion == "1":
        campo = input("1. Asignatura\n2. Fecha\n3. Justificada\n4. Horas\n¿Que quieres modificar?: ").strip()
        if campo == "1":
            _actualizar(id_falta, "asignatura", elegir_asignatura("Nueva asignatura: "))
        elif campo == "2":
            _actualizar(id_falta, "fecha", pedir_fecha())
        elif campo == "3":
            justificada = input("¿Es justificada? (S/N): ").strip().upper() == "S"
            _actualizar(id_falta, "justificada", int(justificada))
        elif campo == "4":
            _actualizar(id_falta, "horas", int(input("Nuevas horas: ")))
        else:
            print("Opcion incorrecta")
            input("Pulsa enter para continuar")
            return
        print("Falta modificada")
    else:
        print("Opcion incorrecta")

    input("Pulsa enter para continuar")
