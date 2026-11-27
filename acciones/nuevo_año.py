import os

from acciones.db_check import DB_PATH


def nuevo_año():

    #Termina el año escolar borrando la base de datos. Devuelve True si se ha borrado, para que el menu cierre el programa

    os.system("cls")
    print("¿Seguro que quieres terminar el año escolar?")
    print("Se borrarán todas tus faltas, tus asignaturas y el porcentaje máximo, y el programa se cerrará.")
    print("No se puede deshacer.")

    decision = ""
    while decision not in ("s", "n"):
        decision = input("¿Quieres borrarlo todo? (S/N): ").strip().lower()
        if decision not in ("s", "n"):
            print("Responde S (sí) o N (no)")

    if decision == "n":
        print("No se ha borrado nada")
        input("Pulsa Enter para continuar")
        return False

    if DB_PATH.exists():
        os.remove(DB_PATH)

    os.system("cls")
    print("Se han borrado todos los datos. La próxima vez que abras el programa empezarás de cero,")
    print("eligiendo el porcentaje y tus asignaturas.")
    print("¡Mucha suerte en tu nuevo año escolar!")
    input("Pulsa Enter para salir")
    return True
