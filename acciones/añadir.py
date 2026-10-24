from asignaturas import asignaturas
ASIGNATURAS = asignaturas

def añadir(asignatura, total_horas, dia, mes, año, justificada):
    """Esta funcion sirve para que el usuario pueda añadir faltas de asistencia a la base de datos. La base de datos
    necesita saber el id (cada falta incrementa ese numero en 1), sirve para llevar el control de todas las faltas en
     general, pero cada asignatura tiene que llevar su propio conteo de faltas. Por ejemplo: puedes tener 5 faltas de
     asignatura X, y en id puede poner 10. La base de datos tambien nececita saber la asignatura a la que has faltado,
     la fecha, si la falta es justificada o no, y el total de horas que el usuario ha faltado (porque hay materias que
     se imparten varias horas seguidas"""

    asignatura = int(int("Elige la asignatura a la que has faltado: ")) #Aqui deberian mostrarse las asignaturas, cada
    #una con su numero
    total_horas = int(int("¿Cuantas horas has faltado?: "))
    dia = int(input("¿Que dia?: "))
    mes = int(input("¿Que mes?: "))
    año = int(input("¿Que año?: "))

    #Con esta informacion, llama a la base de datos para añadir la falta correspondiente