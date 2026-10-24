from acciones.añadir import añadir
from acciones.consultar import consultar
from acciones.modificar import modificar

def menu():

    #Menu principal del proyecto

    #Mensaje de saludo
    bienvenida = "Bienvenido al menu principal"
    print("-"*len(bienvenida))
    print(bienvenida)
    print("-"*len(bienvenida))

    """Opciones disponibles = 1 (añadir falta),
    2 (consultar faltas),
    3 (modificar faltas)"""

    while True:
        eleccion = None

        while "1" or "2," or "3" in eleccion:
            eleccion = input("Elije una opcion: ")

            if eleccion == "1":
                añadir()
            elif eleccion == "2":
                consultar()
            elif eleccion == "3":
                modificar()
            elif eleccion == "4":
                exit()

        print("Opcion incorrecta. Asegurate de introducir un numero del 1 al 4")