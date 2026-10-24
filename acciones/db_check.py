import sqlite3

def comprobar_db():

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asignatura TEXT,
            fecha TEXT,
            justificada TEXT
        )
    """)
    conexion.commit()

    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()
    print(resultados)

    conexion.close()