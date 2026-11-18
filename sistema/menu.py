import os

from acciones.añadir import añadir
from acciones.consultar import consultar
from acciones.materias import materias
from acciones.modificar import modificar
from acciones.nuevo_año import nuevo_año


def menu():

    #Menu principal del proyecto

    """Opciones disponibles = 1 (añadir falta),
    2 (consultar faltas),
    3 (modificar faltas),
    4 (gestionar asignaturas),
    5 (año nuevo)
    6 (salir del programa)"""

    acciones = {"1": añadir, "2": consultar, "3": modificar, "4": materias}
    bienvenida = "Bienvenido al menu principal"
    aviso = ""

    try:
        while True:
            os.system("cls")
            print("-" * len(bienvenida))
            print(bienvenida)
            print("-" * len(bienvenida))
            if aviso:
                print(aviso)
                aviso = ""

            eleccion = input("Elije una opcion. 1. Añadir falta, 2. Consultar falta, 3. Modificar falta, "
                             "4. Gestionar asignaturas, 5. Terminar año, 6. Salir: ").strip()

            if eleccion == "6":
                return
            if eleccion == "5":
                if nuevo_año():
                    return
            elif eleccion in acciones:
                acciones[eleccion]()
            else:
                aviso = "Opcion incorrecta. Asegurate de introducir un numero del 1 al 6"
    except (KeyboardInterrupt, EOFError):
        print("\nHasta pronto")
