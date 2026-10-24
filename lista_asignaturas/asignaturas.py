"""Una asignatura puede tener 33, 66, 99 o 132 horas en todo el ciclo. Es importante saber exactamente cuantas horas
dura cada asignatura ya que las faltas no se cuentan globalmente, sino individualmente"""

ASIGNATURAS = {
    "Sistemes Operatius Monolloc": 99,
    "Sostenibilitat": 33,
    "Angles": 33,
    "Ofimatica": 99,
    "IPO": 99,
    "Muntatge i Manteniment d'Equips": 132,
    "Xarxes Locals": 33,
    "Tutoria": 33,
    "Digitalitzacio": 132,
    "Seguretat Informatica": 99,
}

def asignaturas():
    return ASIGNATURAS

