from acciones.db_check import conectar


def _leer_porcentaje():
    with conectar() as con:
        fila = con.execute("SELECT valor FROM config WHERE clave = 'porcentaje_maximo'").fetchone()
    return int(fila[0]) if fila else None


def _guardar_porcentaje(porcentaje):
    with conectar() as con:
        con.execute("INSERT OR REPLACE INTO config (clave, valor) VALUES ('porcentaje_maximo', ?)", (str(porcentaje),))


def _pedir_entero(pregunta, minimo, maximo):
    while True:
        valor = input(pregunta).strip()
        if valor.isdecimal() and minimo <= int(valor) <= maximo:
            return int(valor)
        print("Introduce un numero entre {} y {}".format(minimo, maximo))


def configurar_porcentaje():
    """Si todavia no esta establecido, pregunta que porcentaje de horas se puede faltar por modulo y lo guarda."""
    if _leer_porcentaje() is not None:
        return
    print("Todavia no has indicado que porcentaje de las horas de cada modulo puedes faltar.")
    porcentaje = _pedir_entero("¿Que porcentaje de horas puedes faltar por modulo? (1-100): ", 1, 100)
    _guardar_porcentaje(porcentaje)
    print("Porcentaje guardado: {}%".format(porcentaje))
    input("Pulsa enter para continuar")
