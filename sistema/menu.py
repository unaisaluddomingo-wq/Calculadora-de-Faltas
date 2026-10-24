import os

from acciones.añadir import añadir
from acciones.consultar import consultar
from acciones.modificar import modificar


def menu():

    #Menu principal del proyecto

    """Opciones disponibles = 1 (añadir falta),
    2 (consultar faltas),
    3 (modificar faltas),
    4 (salir del programa)"""

    acciones = {"1": añadir, "2": consultar, "3": modificar}
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

            eleccion = input("Elije una opcion. 1. Añadir falta, 2. Consultar falta, 3. Modificar falta, 4. Salir: ").strip()

            if eleccion == "4":
                return
            if eleccion in acciones:
                acciones[eleccion]()
            else:
                aviso = "Opcion incorrecta. Asegurate de introducir un numero del 1 al 4"
    except (KeyboardInterrupt, EOFError):
        print("\nHasta pronto")
