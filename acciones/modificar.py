import msvcrt
import os
import time
from datetime import date

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
            for fila in filas:
                if str(fila[0]).rstrip(".") == escrito:
                    print()
                    return fila
            aviso = "No hay ninguna opción con el número {}".format(escrito) if escrito else "Escribe un número y pulsa Enter"
            escrito = ""
        elif tecla == "\b":
            escrito = escrito[:-1]
        elif tecla == "\x03":
            raise KeyboardInterrupt
        elif tecla.isdigit():
            escrito += tecla


def _elegir_asignatura(pregunta):
    filas = [("{}.".format(i), nombre) for i, nombre in enumerate(asignaturas(), start=1)]
    fila = _elegir(["N.", "Asignatura"], filas, pregunta)
    return None if fila is None else fila[1]


def _pedir_entero(pregunta, minimo, maximo):
    while True:
        valor = input(pregunta).strip()
        if valor.isdecimal() and minimo <= int(valor) <= maximo:
            return int(valor)
        print("Escribe un número entre {} y {}".format(minimo, maximo))


def _pedir_fecha(pregunta):
    """Pide la fecha como DD/MM/AAAA (Enter vacio = hoy) hasta que es real y no futura. La devuelve como AAAA-MM-DD."""
    hoy = date.today()
    while True:
        texto = input(pregunta).strip()
        if not texto:
            return hoy.isoformat()
        partes = texto.replace("-", "/").replace(".", "/").split("/")
        if len(partes) != 3 or not all(parte.isdecimal() for parte in partes):
            print("Escribe la fecha como DD/MM/AAAA, por ejemplo {}".format(hoy.strftime("%d/%m/%Y")))
            continue
        dia, mes, año = (int(parte) for parte in partes)
        if año < 100:
            año += 2000  # 27/11/26 -> 2026
        try:
            fecha = date(año, mes, dia)
        except ValueError:
            print("Esa fecha no existe, vuelve a escribirla")
            continue
        if fecha > hoy:
            print("La fecha no puede ser posterior a hoy")
        elif fecha.year < 2000:
            print("Escribe un año a partir del 2000")
        else:
            return fecha.isoformat()


def _dd_mm_aaaa(fecha):
    """AAAA-MM-DD (como se guarda) -> DD/MM/AAAA (como se escribe y se lee en España)."""
    return date.fromisoformat(fecha).strftime("%d/%m/%Y")


def _pedir_si_no(pregunta):
    while True:
        respuesta = input(pregunta).strip().upper()
        if respuesta in ("S", "N"):
            return respuesta == "S"
        print("Responde S (sí) o N (no)")


def _pedir_opcion(pregunta, opciones):
    while True:
        opcion = input(pregunta).strip()
        if opcion in opciones:
            return opcion
        print("Esa opción no existe. Escribe uno de estos números: {}".format(", ".join(opciones)))


def _actualizar(id_falta, campo, valor):
    # campo siempre viene de las opciones fijas de modificar(), nunca del usuario
    with conectar() as con:
        con.execute("UPDATE faltas SET {} = ? WHERE id = ?".format(campo), (valor, id_falta))


def modificar():
    with conectar() as con:
        # las mas recientes primero, que suelen ser las que se quieren corregir
        faltas = con.execute("SELECT id, asignatura, fecha, horas, justificada FROM faltas ORDER BY id DESC").fetchall()
    if not faltas:
        print("Todavía no hay faltas registradas. Añade una con la opción 1 del menú.")
        input("Pulsa Enter para continuar")
        return

    filas = [(id_falta, asignatura, _dd_mm_aaaa(fecha), horas, "S" if justificada else "N")
             for id_falta, asignatura, fecha, horas, justificada in faltas]
    fila = _elegir(["ID", "Asignatura", "Fecha", "Horas", "Justificada"], filas,
                   "Escribe el ID de la falta que quieres cambiar y pulsa Enter: ")
    if fila is None:
        return
    id_falta, asignatura, fecha, horas, justificada = fila
    descripcion = "la falta {} ({}, {}, {} h)".format(id_falta, asignatura, fecha, horas)

    accion = _pedir_opcion("¿Qué quieres hacer con {}?\n1. Modificarla\n2. Borrarla\n0. Volver al menú\n"
                           "Elige una opción: ".format(descripcion), ("1", "2", "0"))
    if accion == "0":
        return
    if accion == "2":
        if _pedir_si_no("¿Seguro que quieres borrar {}? No se puede deshacer (S/N): ".format(descripcion)):
            with conectar() as con:
                con.execute("DELETE FROM faltas WHERE id = ?", (id_falta,))
            print("Falta borrada")
        else:
            print("No se ha borrado la falta")
    else:
        campo = _pedir_opcion("1. Asignatura (ahora: {})\n2. Fecha (ahora: {})\n3. Justificada (ahora: {})\n"
                              "4. Horas (ahora: {})\n0. Volver al menú\n¿Qué quieres modificar?: "
                              .format(asignatura, fecha, justificada, horas), ("1", "2", "3", "4", "0"))
        if campo == "0":
            return
        if campo == "1":
            nueva = _elegir_asignatura("¿A qué asignatura pertenece la falta? Escribe su número y pulsa Enter: ")
            if nueva is None:
                return
            _actualizar(id_falta, "asignatura", nueva)
        elif campo == "2":
            _actualizar(id_falta, "fecha", _pedir_fecha("Nueva fecha (DD/MM/AAAA, pulsa Enter si es hoy): "))
        elif campo == "3":
            _actualizar(id_falta, "justificada", int(_pedir_si_no("¿Es justificada? (S/N): ")))
        else:
            _actualizar(id_falta, "horas", _pedir_entero("Nuevas horas (1-24): ", 1, 24))
        print("Falta modificada")

    input("Pulsa Enter para continuar")
