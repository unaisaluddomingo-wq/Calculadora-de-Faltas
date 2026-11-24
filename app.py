"""Version grafica de la Calculadora de Faltas (la de terminal sigue siendo main.py). Arranca un servidor local y
abre la app en una ventana propia de Microsoft Edge (modo aplicacion, sin barra de direcciones). Si no hay Edge, la
abre en el navegador por defecto. El programa termina al cerrar la ventana o al terminar el año escolar."""
import os
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

from acciones.db_check import comprobar_db
from interfaz.servidor import crear_servidor


def _buscar_edge():
    encontrado = shutil.which("msedge")
    if encontrado:
        return encontrado
    for carpeta in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"):
        base = os.environ.get(carpeta)
        if base:
            ruta = Path(base) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
            if ruta.exists():
                return str(ruta)
    return None


def _abrir_ventana(url):
    """Abre la ventana de la app. Devuelve el proceso de Edge (para saber cuando se cierra) o None."""
    edge = _buscar_edge()
    if edge is None:
        webbrowser.open(url)
        return None
    # un perfil propio hace que la ventana sea un proceso aparte que termina al cerrarla
    perfil = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "CalculadoraDeFaltas" / "ventana"
    return subprocess.Popen([edge, "--app={}".format(url), "--user-data-dir={}".format(perfil),
                             "--window-size=1120,840", "--no-first-run", "--no-default-browser-check"])


def main():
    comprobar_db()
    servidor = crear_servidor()
    url = "http://127.0.0.1:{}/".format(servidor.server_port)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()

    ventana = _abrir_ventana(url)
    abierta = time.monotonic()
    print("Calculadora de Faltas abierta en {}".format(url))
    print("Para salir cierra la ventana de la app o pulsa Ctrl+C aqui")

    try:
        while hilo.is_alive():
            if ventana is not None and ventana.poll() is not None:
                if time.monotonic() - abierta > 5:
                    break  # el usuario ha cerrado la ventana
                # Edge ha terminado enseguida: ya habia otra ventana de la app y se la ha pasado. Seguimos hasta Ctrl+C
                ventana = None
            hilo.join(0.3)
    except KeyboardInterrupt:
        pass

    servidor.shutdown()
    servidor.server_close()
    print("Hasta pronto")


if __name__ == "__main__":
    main()
