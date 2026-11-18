import os

from acciones.db_check import DB_PATH


def nuevo_año():

    #Termina el año escolar borrando la base de datos. Devuelve True si se ha borrado, para que el menu cierre el programa

    os.system("cls")
    print("¿Estas seguro de que deseas terminar el año escolar?")
    print("Esta accion eliminara la base de datos con todas tus faltas de asistencia, asignaturas registradas y demas informacion")
    print("Esta accion no es reversible")

    decision = ""
    while decision not in ("s", "n"):
        decision = input("¿Deseas continuar [S/N]? ").strip().lower()
        if decision not in ("s", "n"):
            print("Respuesta no valida. Escribe S o N")

    if decision == "n":
        print("No se ha borrado nada")
        input("Pulsa enter para continuar...")
        return False

    if DB_PATH.exists():
        os.remove(DB_PATH)

    os.system("cls")
    print("Se ha borrado la base de datos y con ella todos los datos, al volver a encender el programa aparecera")
    print("todo el proceso de configuracion")
    print("¡Mucha suerte en tu nuevo año escolar!")
    input("Pulsa enter para salir...")
    return True
