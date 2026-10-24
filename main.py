from acciones.db_check import comprobar_db
from menu import menu

def main():
    comprobar_db()
    menu()

if __name__ == "__main__":
    main()