"""Una asignatura puede tener 33, 66, 99 o 132 horas en todo el ciclo. Es importante saber exactamente cuantas horas
dura cada asignatura ya que las faltas no se cuentan globalmente, sino individualmente"""

#Transforma esta lista de asignaturas en un diccionario e indica cuantas horas dura cada asignatura, en orden, te las
#dejo ordenadas (elimina este comentario cuando acabes): 99, 33, 33, 99, 99, 132, 33, 33, 132, 99

ASIGNATURAS = ["Sistemes Operatius Monolloc", "Sostenibilitat", "Angles",
               "Ofimatica", "IPO", "Muntatge i Manteniment d'Equips",
               "Xarxes Locals", "Tutoria", "Digitalitzacio", "Seguretat Informatica"]

def asignaturas():
    return ASIGNATURAS