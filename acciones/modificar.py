import msvcrt
import os
from datetime import date

from acciones.db_check import conectar
from lista_asignaturas.asignaturas import asignaturas

POR_PAGINA = 5


def _tabla(cabeceras, filas):
    """Devuelve el texto de una tabla en ASCII al estilo del cliente de MySQL."""
    anchos = [max(len(str(celda)) for celda in columna) for columna in zip(cabeceras, *filas)]
    separador = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"

    def linea(celdas):
        return "|" + "|".join(" {} ".format(str(celda).ljust(ancho)) for celda, ancho in zip(celdas, anchos)) + "|"

    return "\n".join([separador, linea(cabeceras), separador] + [linea(fila) for fila in filas] + [separador])


def _elegir(cabeceras, filas, pregunta):
    """Muestra la tabla de 5 en 5 (flechas para cambiar de pagina) y devuelve la fila elegida.
    El usuario escribe el contenido de la primera columna (sin el punto final, si lo tiene)."""
    paginas = (len(filas) - 1) // POR_PAGINA + 1
    pagina = 0
    escrito = ""
    aviso = ""
    while True:
        os.system("cls")
        print("\033[3J\033[H", end="")  # borra tambien lo que quede en el historial de la terminal
        inicio = pagina * POR_PAGINA
        print(_tabla(cabeceras, filas[inicio:inicio + POR_PAGINA]))
        print("Pagina {}/{} (usa las flechas para cambiar de pagina)".format(pagina + 1, paginas))
        if aviso:
            print(aviso)
            aviso = ""
        print("{}{}".format(pregunta, escrito), end="", flush=True)

        tecla = msvcrt.getwch()
        flecha = ""
        if tecla in ("\x00", "\xe0"):
            flecha = msvcrt.getwch()
        elif tecla == "\x1b" and msvcrt.kbhit():
            # algunas terminales envian las flechas como secuencias ANSI: ESC [ A/B/C/D
            if msvcrt.getwch() in ("[", "O") and msvcrt.kbhit():
                flecha = {"A": "H", "B": "P", "C": "M", "D": "K"}.get(msvcrt.getwch(), "")
        if flecha:
            if flecha in ("K", "H"):
                pagina = max(pagina - 1, 0)
            elif flecha in ("M", "P"):
                pagina = min(pagina + 1, paginas - 1)
        elif tecla == "\r":
            for fila in filas:
                if str(fila[0]).rstrip(".") == escrito:
                    print()
                    return fila
            aviso = "Opcion incorrecta"
            escrito = ""
        elif tecla == "\b":
            escrito = escrito[:-1]
        elif tecla == "\x03":
            raise KeyboardInterrupt
        elif tecla.isdigit():
            escrito += tecla


def _elegir_asignatura(pregunta):
    filas = [("{}.".format(i), nombre) for i, nombre in enumerate(asignaturas(), start=1)]
    return _elegir(["N.", "Asignatura"], filas, pregunta)[1]


def _pedir_entero(pregunta, minimo, maximo):
    while True:
        valor = input(pregunta).strip()
        if valor.isdecimal() and minimo <= int(valor) <= maximo:
            return int(valor)
        print("Introduce un numero entre {} y {}".format(minimo, maximo))


def _pedir_fecha():
    """Pide dia, mes y año hasta que forman una fecha real y la devuelve como AAAA-MM-DD."""
    while True:
        dia = _pedir_entero("¿Que dia?: ", 1, 31)
        mes = _pedir_entero("¿Que mes?: ", 1, 12)
        año = _pedir_entero("¿Que año?: ", 2000, 2100)
        try:
            return date(año, mes, dia).isoformat()
        except ValueError:
            print("Esa fecha no existe, vuelve a introducirla")


def _pedir_si_no(pregunta):
    while True:
        respuesta = input(pregunta).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("Responde S o N")


def _pedir_opcion(pregunta, opciones):
    while True:
        opcion = input(pregunta).strip()
        if opcion in opciones:
            return opcion
        print("Opcion incorrecta")


def _actualizar(id_falta, campo, valor):
    # campo siempre viene de las opciones fijas de modificar(), nunca del usuario
    with conectar() as con:
        con.execute("UPDATE faltas SET {} = ? WHERE id = ?".format(campo), (valor, id_falta))


def modificar():
    with conectar() as con:
        faltas = con.execute("SELECT id, asignatura, fecha, horas, justificada FROM faltas ORDER BY id").fetchall()
    if not faltas:
        print("No hay faltas registradas")
        input("Pulsa enter para continuar")
        return

    filas = [(id_falta, asignatura, fecha, horas, "S" if justificada else "N")
             for id_falta, asignatura, fecha, horas, justificada in faltas]
    id_falta = _elegir(["ID", "Asignatura", "Fecha", "Horas", "Justificada"], filas,
                       "Elige la falta de asistencia que deseas modificar (id): ")[0]

    accion = _pedir_opcion("1. Modificar\n2. Borrar\nElige una opcion: ", ("1", "2"))
    if accion == "2":
        if _pedir_si_no("¿Seguro que quieres borrarla? (S/N): "):
            with conectar() as con:
                con.execute("DELETE FROM faltas WHERE id = ?", (id_falta,))
            print("Falta borrada")
        else:
            print("No se ha borrado la falta")
    else:
        campo = _pedir_opcion("1. Asignatura\n2. Fecha\n3. Justificada\n4. Horas\n¿Que quieres modificar?: ",
                              ("1", "2", "3", "4"))
        if campo == "1":
            _actualizar(id_falta, "asignatura", _elegir_asignatura("Nueva asignatura: "))
        elif campo == "2":
            _actualizar(id_falta, "fecha", _pedir_fecha())
        elif campo == "3":
            _actualizar(id_falta, "justificada", int(_pedir_si_no("¿Es justificada? (S/N): ")))
        else:
            _actualizar(id_falta, "horas", _pedir_entero("Nuevas horas: ", 1, 24))
        print("Falta modificada")

    input("Pulsa enter para continuar")
