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
    bienvenida = "Calculadora de Faltas - Menú principal"
    aviso = ""

    try:
        while True:
            os.system("cls")
            print("-" * len(bienvenida))
            print(bienvenida)
            print("-" * len(bienvenida))
            print("1. Añadir una falta")
            print("2. Consultar mis faltas")
            print("3. Modificar o borrar una falta")
            print("4. Gestionar asignaturas")
            print("5. Terminar el año escolar (borra todos los datos)")
            print("6. Salir")
            if aviso:
                print(aviso)
                aviso = ""

            eleccion = input("Elige una opción (1-6): ").strip()

            if eleccion == "6":
                return
            if eleccion == "5":
                if nuevo_año():
                    return
            elif eleccion in acciones:
                acciones[eleccion]()
            else:
                aviso = "Esa opción no existe. Escribe un número del 1 al 6"
    except (KeyboardInterrupt, EOFError):
        print("\nHasta pronto")
