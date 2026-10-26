import msvcrt
import os

from acciones.db_check import conectar

POR_PAGINA = 5
MAX_HORAS = 800


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


def _pedir_entero(pregunta, minimo, maximo):
    while True:
        valor = input(pregunta).strip()
        if valor.isdecimal() and minimo <= int(valor) <= maximo:
            return int(valor)
        print("Introduce un numero entre {} y {}".format(minimo, maximo))


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


def _pedir_nombre(pregunta, ignorar=None):
    """Pide un nombre no vacio que no tenga ya otra asignatura (sin distinguir mayusculas).
    ignorar es el nombre actual de la asignatura que se esta renombrando."""
    existentes = [nombre.lower() for nombre in _leer_asignaturas() if nombre != ignorar]
    while True:
        nombre = input(pregunta).strip()
        if not nombre or len(nombre) > 60:
            print("El nombre debe tener entre 1 y 60 caracteres")
        elif nombre.lower() in existentes:
            print("Ya existe una asignatura con ese nombre")
        else:
            return nombre


def _pedir_horas():
    return _pedir_entero("¿Cuantas horas tiene la asignatura en todo el año? (1-{}): ".format(MAX_HORAS), 1, MAX_HORAS)


def _leer_asignaturas():
    with conectar() as con:
        return dict(con.execute("SELECT nombre, horas FROM asignaturas ORDER BY rowid").fetchall())


def _crear(nombre, horas):
    with conectar() as con:
        con.execute("INSERT INTO asignaturas (nombre, horas) VALUES (?, ?)", (nombre, horas))


def _elegir_asignatura(pregunta):
    filas = [("{}.".format(i), nombre, horas) for i, (nombre, horas) in enumerate(_leer_asignaturas().items(), start=1)]
    fila = _elegir(["N.", "Asignatura", "Horas"], filas, pregunta)
    return fila[1], fila[2]


def _renombrar(nombre, nuevo):
    """Cambia el nombre y tambien el de las faltas ya registradas de esa asignatura."""
    with conectar() as con:
        con.execute("UPDATE asignaturas SET nombre = ? WHERE nombre = ?", (nuevo, nombre))
        con.execute("UPDATE faltas SET asignatura = ? WHERE asignatura = ?", (nuevo, nombre))


def _cambiar_horas(nombre, horas):
    with conectar() as con:
        con.execute("UPDATE asignaturas SET horas = ? WHERE nombre = ?", (horas, nombre))


def _borrar(nombre):
    """Borra la asignatura y sus faltas. Devuelve cuantas faltas se han borrado."""
    with conectar() as con:
        borradas = con.execute("DELETE FROM faltas WHERE asignatura = ?", (nombre,)).rowcount
        con.execute("DELETE FROM asignaturas WHERE nombre = ?", (nombre,))
    return borradas


def _contar_faltas(nombre):
    with conectar() as con:
        return con.execute("SELECT COUNT(*) FROM faltas WHERE asignatura = ?", (nombre,)).fetchone()[0]


def _añadir_una():
    nombre = _pedir_nombre("Nombre de la asignatura: ")
    _crear(nombre, _pedir_horas())
    print("Asignatura creada")


def configuracion_inicial():
    """Si no hay ninguna asignatura obliga a crear al menos una; despues deja añadir mas."""
    if _leer_asignaturas():
        return
    os.system("cls")
    print("No hay ninguna asignatura registrada. Tienes que añadir al menos una.")
    while True:
        _añadir_una()
        if not _pedir_si_no("¿Quieres añadir otra asignatura? (S/N, N para pasar al programa): "):
            return


def materias():
    while True:
        os.system("cls")
        opcion = _pedir_opcion(
            "1. Crear asignatura\n2. Eliminar asignatura\n3. Cambiar nombre\n4. Cambiar horas\n5. Volver\n"
            "Elige una opcion: ", ("1", "2", "3", "4", "5"))
        if opcion == "5":
            return

        if opcion == "1":
            _añadir_una()
        elif opcion == "2":
            if len(_leer_asignaturas()) == 1:
                print("No puedes eliminar la unica asignatura que hay")
            else:
                nombre, _ = _elegir_asignatura("Elige la asignatura a eliminar (N.): ")
                faltas = _contar_faltas(nombre)
                if _pedir_si_no("¿Seguro que quieres eliminar {}? Se borraran tambien sus {} faltas (S/N): "
                                .format(nombre, faltas)):
                    _borrar(nombre)
                    print("Asignatura eliminada")
                else:
                    print("No se ha eliminado la asignatura")
        elif opcion == "3":
            nombre, _ = _elegir_asignatura("Elige la asignatura a renombrar (N.): ")
            _renombrar(nombre, _pedir_nombre("Nuevo nombre: ", ignorar=nombre))
            print("Nombre cambiado")
        else:
            nombre, _ = _elegir_asignatura("Elige la asignatura a la que cambiar las horas (N.): ")
            _cambiar_horas(nombre, _pedir_horas())
            print("Horas cambiadas")

        input("Pulsa enter para continuar")
