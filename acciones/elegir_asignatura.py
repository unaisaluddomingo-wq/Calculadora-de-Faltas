from lista_asignaturas.asignaturas import asignaturas


def elegir_asignatura(pregunta):
    """Muestra las asignaturas numeradas y devuelve el nombre de la elegida."""
    nombres = list(asignaturas())
    for i, nombre in enumerate(nombres, start=1):
        print("{}. {}".format(i, nombre))
    while True:
        eleccion = input(pregunta)
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(nombres):
            return nombres[int(eleccion) - 1]
        print("Numero de asignatura incorrecto")
