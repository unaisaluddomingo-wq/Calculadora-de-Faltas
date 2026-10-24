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
            fecha = date(año, mes, dia)
            if fecha > date.today():
                print("La fecha no puede ser futura")
                continue
            return fecha.isoformat()
        except ValueError:
            print("Esa fecha no existe, vuelve a introducirla")


def _pedir_si_no(pregunta):
    while True:
        respuesta = input(pregunta).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("Responde S o N")


def añadir():
    nombre = _elegir_asignatura("Elige la asignatura a la que has faltado: ")
    total_horas = _pedir_entero("¿Cuantas horas has faltado?: ", 1, 24)
    fecha = _pedir_fecha()
    justificada = _pedir_si_no("¿Es justificada? (S/N): ")

    with conectar() as con:
        con.execute(
            "INSERT INTO faltas (asignatura, fecha, justificada, horas) VALUES (?, ?, ?, ?)",
            (nombre, fecha, int(justificada), total_horas),
        )
    print("Falta de asistencia registrada")
    input("Pulsa enter para continuar")
