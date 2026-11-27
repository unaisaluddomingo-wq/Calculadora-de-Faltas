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
        print("Escribe un número entre {} y {}".format(minimo, maximo))


def configurar_porcentaje():
    """Si todavia no esta establecido, pregunta que porcentaje de horas se puede faltar por modulo y lo guarda."""
    if _leer_porcentaje() is not None:
        return
    print("Bienvenido a la Calculadora de Faltas. Antes de empezar hay que configurarla.")
    print("Primero: ¿qué porcentaje de las horas de cada asignatura puedes faltar sin suspenderla?")
    print("Lo decide tu centro (en muchos es el 20%).")
    porcentaje = _pedir_entero("Porcentaje máximo de faltas (1-100): ", 1, 100)
    _guardar_porcentaje(porcentaje)
    print("Porcentaje guardado: {}%".format(porcentaje))
    input("Pulsa Enter para continuar")
