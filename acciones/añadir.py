from menu import menu
from asignaturas import asignaturas
ASIGNATURAS = asignaturas

def añadir(asignatura, total_horas, dia, mes, año, justificada):
    asignatura = int(int("Elige la asignatura a la que has faltado: ")) #Aqui deberian mostrarse las asignaturas
    # ordenadas, cada una con su numero
    total_horas = int(int("¿Cuantas horas has faltado?: "))
    dia = int(input("¿Que dia?: "))
    mes = int(input("¿Que mes?: "))
    año = int(input("¿Que año?: "))

    #Aqui la orden de llamar a la base de datos con toda la info del usuario y añadir la falta.
    print ("Falta de asistencia registrada")
    menu()