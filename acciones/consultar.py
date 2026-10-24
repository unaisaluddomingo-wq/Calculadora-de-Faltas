import msvcrt
import os

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


def _elegir_asignatura(pregunta):
    """Muestra las asignaturas de 5 en 5 (flechas para cambiar de pagina) y devuelve el nombre de la elegida."""
    filas = [("{}.".format(i), nombre) for i, nombre in enumerate(asignaturas(), start=1)]
    paginas = (len(filas) - 1) // POR_PAGINA + 1
    pagina = 0
    escrito = ""
    aviso = ""
    while True:
        os.system("cls")
        print("\033[3J\033[H", end="")  # borra tambien lo que quede en el historial de la terminal
        inicio = pagina * POR_PAGINA
        print(_tabla(["N.", "Asignatura"], filas[inicio:inicio + POR_PAGINA]))
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
            for numero, nombre in filas:
                if numero.rstrip(".") == escrito:
                    print()
                    return nombre
            aviso = "Numero de asignatura incorrecto"
            escrito = ""
        elif tecla == "\b":
            escrito = escrito[:-1]
        elif tecla == "\x03":
            raise KeyboardInterrupt
        elif tecla.isdigit():
            escrito += tecla


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
    todas = asignaturas()
    while True:
        opcion = input("1. Ver faltas totales\n2. Ver faltas de una asignatura\nElige una opcion: ").strip()
        if opcion in ("1", "2"):
            break
        print("Opcion incorrecta")

    if opcion == "1":
        print("Faltas totales: {}/{}".format(_horas_faltadas(), sum(todas.values())))
    else:
        nombre = _elegir_asignatura("Introduce que asignatura quieres consultar: ")
        print("{}: {}/{}".format(nombre, _horas_faltadas(nombre), todas[nombre]))

    input("Pulsa enter para continuar")
