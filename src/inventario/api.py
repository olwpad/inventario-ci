"""Servidor HTTP mínimo (solo librería estándar) para poder probar el contenedor.

GET /salud       -> {"estado": "ok", "version": "..."}
GET /inventario  -> productos de ejemplo y valor total
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import __version__
from .core import Inventario

inventario = Inventario()
inventario.agregar("sensor-dht22", 10, 12500)
inventario.agregar("arduino-uno-r4", 3, 98000)


class Manejador(BaseHTTPRequestHandler):
    def _responder(self, codigo: int, cuerpo: dict) -> None:
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        if self.path == "/salud":
            self._responder(200, {"estado": "ok", "version": __version__})
        elif self.path == "/inventario":
            self._responder(200, {"productos": inventario.como_dict(),
                                  "valor_total": inventario.valor_total()})
        else:
            self._responder(404, {"error": "ruta no encontrada"})


def main(puerto: int = 8000) -> None:
    print(f"Inventario {__version__} escuchando en el puerto {puerto}", flush=True)
    HTTPServer(("0.0.0.0", puerto), Manejador).serve_forever()


if __name__ == "__main__":
    main()
