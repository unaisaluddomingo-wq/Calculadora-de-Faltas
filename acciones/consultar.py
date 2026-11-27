import msvcrt
import os
import time

from acciones.db_check import conectar
from lista_asignaturas.obtener_asignaturas import asignaturas

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
        if paginas > 1:
            print("Página {}/{} (usa las flechas para cambiar de página)".format(pagina + 1, paginas))
        print("0. Volver sin elegir (o pulsa Esc)")
        if aviso:
            print(aviso)
            aviso = ""
        print("{}{}".format(pregunta, escrito), end="", flush=True)

        tecla = msvcrt.getwch()
        flecha = ""
        if tecla in ("\x00", "\xe0"):
            flecha = msvcrt.getwch()
        elif tecla == "\x1b":
            time.sleep(0.05)  # deja llegar el resto de la secuencia si es una flecha y no un Esc
            if not msvcrt.kbhit():
                print()
                return None  # Esc solo: volver sin elegir nada
            # algunas terminales envian las flechas como secuencias ANSI: ESC [ A/B/C/D
            if msvcrt.getwch() in ("[", "O") and msvcrt.kbhit():
                flecha = {"A": "H", "B": "P", "C": "M", "D": "K"}.get(msvcrt.getwch(), "")
        if flecha:
            if flecha in ("K", "H"):
                pagina = max(pagina - 1, 0)
            elif flecha in ("M", "P"):
                pagina = min(pagina + 1, paginas - 1)
        elif tecla == "\r":
            if escrito == "0":
                print()
                return None
            for numero, nombre in filas:
                if numero.rstrip(".") == escrito:
                    print()
                    return nombre
            aviso = "No hay ninguna asignatura con el número {}".format(escrito) if escrito else "Escribe un número y pulsa Enter"
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


def _leer_porcentaje():
    with conectar() as con:
        fila = con.execute("SELECT valor FROM config WHERE clave = 'porcentaje_maximo'").fetchone()
    return int(fila[0]) if fila else None


def _aviso_limite(nombre, faltas, total):
    limite = _leer_porcentaje()
    if limite is not None and faltas * 100 > limite * total:
        print("¡ALERTA! {}: {:.1f}% de faltas; has superado el límite del {}%.".format(nombre, faltas / total * 100, limite))


def consultar():
    todas = asignaturas()
    os.system("cls")
    while True:
        opcion = input("1. Ver el total de horas faltadas\n2. Ver una asignatura\n0. Volver al menú\n"
                       "Elige una opción: ").strip()
        if opcion in ("1", "2", "0"):
            break
        print("Esa opción no existe. Escribe 1, 2 o 0")

    if opcion == "0":
        return

    if opcion == "1":
        print("Faltas totales: {}/{} horas".format(_horas_faltadas(), sum(todas.values())))
        for nombre, total in todas.items():
            _aviso_limite(nombre, _horas_faltadas(nombre), total)
    else:
        nombre = _elegir_asignatura("¿Qué asignatura quieres consultar? Escribe su número y pulsa Enter: ")
        if nombre is None:
            return
        faltas = _horas_faltadas(nombre)
        total = todas[nombre]
        print("{}: {}/{} horas faltadas".format(nombre, faltas, total))
        limite = _leer_porcentaje()
        if limite is not None and faltas * 100 <= limite * total:
            # horas enteras que aun se pueden faltar sin pasar del limite
            print("Puedes faltar {} h más sin pasar del {}%".format(total * limite // 100 - faltas, limite))
        _aviso_limite(nombre, faltas, total)

    input("Pulsa Enter para continuar")
