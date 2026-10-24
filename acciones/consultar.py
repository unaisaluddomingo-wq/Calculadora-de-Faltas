from menu import menu

from asignaturas import asignaturas
ASIGNATURAS = asignaturas

def consultar(asignatura, total_horas, dia, mes, año, justificada):
    pedido = int(input("Introduce que asignatura quieres consultar: "))

menu()