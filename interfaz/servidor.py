"""Servidor local de la interfaz grafica. Sirve la pagina (web/index.html) y responde a sus peticiones en /api/.
Solo escucha en 127.0.0.1, asi que nadie mas de la red puede usarlo. No tiene consultas SQL: cada peticion llama a la
funcion de su accion (faltas.py, asignaturas.py o curso.py)."""
import json
import sqlite3
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from interfaz import asignaturas, curso, faltas

PAGINA = Path(__file__).resolve().parent / "web" / "index.html"

# Peticiones que cambian datos: ruta -> funcion que recibe el diccionario enviado por la pagina
CAMBIOS = {
    "/api/faltas/nueva": faltas.añadir,
    "/api/faltas/modificar": faltas.modificar,
    "/api/faltas/borrar": faltas.borrar,
    "/api/asignaturas/nueva": asignaturas.crear,
    "/api/asignaturas/renombrar": asignaturas.renombrar,
    "/api/asignaturas/horas": asignaturas.cambiar_horas,
    "/api/asignaturas/borrar": asignaturas.eliminar,
    "/api/limite": curso.cambiar_limite,
    "/api/configurar": curso.configurar,
}


def _estado():
    """Todo lo que la pagina necesita para dibujarse."""
    limite = curso.leer_limite()
    lista = asignaturas.listar()
    return {"limite": limite, "asignaturas": lista, "faltas": faltas.listar(),
            "configurado": limite is not None and bool(lista)}


class _Peticiones(BaseHTTPRequestHandler):

    def log_message(self, formato, *args):
        pass  # sin esto se escribiria una linea en la terminal por cada peticion

    def _responder(self, codigo, cuerpo, tipo="application/json; charset=utf-8"):
        if not isinstance(cuerpo, bytes):
            cuerpo = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def _desde_la_app(self):
        """Solo acepta peticiones hechas a esta direccion exacta (evita que otras webs abiertas usen el servidor)."""
        direccion = "127.0.0.1:{}".format(self.server.server_port)
        origen = self.headers.get("Origin")
        return self.headers.get("Host") == direccion and (origen is None or origen == "http://" + direccion)

    def do_GET(self):
        if not self._desde_la_app():
            self._responder(403, {"error": "Peticion no permitida"})
        elif self.path == "/":
            self._responder(200, PAGINA.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/estado":
            self._responder(200, _estado())
        else:
            self._responder(404, {"error": "No existe"})

    def do_POST(self):
        if not self._desde_la_app() or self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            self._responder(403, {"error": "Peticion no permitida"})
            return

        if self.path == "/api/terminar":
            curso.terminar_año()
            self._responder(200, {"terminado": True})
            # el programa se cierra igual que la version de terminal; shutdown() se llama desde otro hilo
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        accion = CAMBIOS.get(self.path)
        if accion is None:
            self._responder(404, {"error": "No existe"})
            return
        try:
            largo = int(self.headers.get("Content-Length") or 0)
            datos = json.loads(self.rfile.read(largo) or b"{}")
            if not isinstance(datos, dict):
                raise ValueError("Datos incorrectos")
            accion(datos)
        except ValueError as error:
            self._responder(400, {"error": str(error)})
            return
        except sqlite3.IntegrityError:
            self._responder(400, {"error": "Esos datos no se pueden guardar"})
            return
        self._responder(200, _estado())


def crear_servidor():
    """Crea el servidor en un puerto libre cualquiera de 127.0.0.1 (server_port dice cual)."""
    return ThreadingHTTPServer(("127.0.0.1", 0), _Peticiones)
