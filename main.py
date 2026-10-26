from acciones.db_check import comprobar_db
from acciones.materias import configuracion_inicial
from acciones.porcentaje import configurar_porcentaje
from acciones.sugerencia import sugerencia
from sistema.menu import menu

def main():
    comprobar_db()
    try:
        configurar_porcentaje()
        configuracion_inicial()
        sugerencia()
    except (KeyboardInterrupt, EOFError):
        print("\nHasta pronto")
        return
    menu()

if __name__ == "__main__":
    main()