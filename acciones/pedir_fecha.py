def pedir_fecha():
    """Pide dia, mes y año al usuario y devuelve la fecha como AAAA-MM-DD."""
    dia = int(input("¿Que dia?: "))
    mes = int(input("¿Que mes?: "))
    año = int(input("¿Que año?: "))
    return "{:04d}-{:02d}-{:02d}".format(año, mes, dia)
