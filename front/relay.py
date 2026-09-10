# -*- coding: utf-8 -*-
"""Servidor local de la consola: sirve el repositorio y, opcionalmente, corre el evaluador.

    set ANTHROPIC_API_KEY=...        (Windows, en la misma terminal)
    python front/relay.py

Y después: http://localhost:8731/front/consola.html

POR QUÉ EXISTE Y DÓNDE ESTÁ LA LÍNEA
------------------------------------
La consola no puede llamar al modelo por sí sola: hacerlo pediría meter una credencial dentro del
navegador, que es la bandera G8 que esta misma rúbrica penaliza. Este archivo mueve la credencial
al único lugar donde corresponde: **el proceso local, leída de una variable de entorno.**

- La key nunca entra al navegador, ni al `localStorage`, ni a un archivo del repositorio.
- No se imprime, no se loguea, no viaja en ninguna respuesta.
- Sin la variable puesta, el relay funciona igual: sirve los archivos y avisa que no puede evaluar.
  El camino de copiar y pegar sigue intacto, y sigue siendo el que se usa en cualquier máquina.

Sin dependencias: sólo biblioteca estándar.
"""
import http.server, json, os, socketserver, ssl, sys, urllib.request, urllib.error

RAIZ    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUERTO  = int(os.environ.get("PUERTO", "8731"))
MODELO  = os.environ.get("MODELO", "claude-sonnet-5")
API     = "https://api.anthropic.com/v1/messages"


def hay_key():
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def evaluar(prompt):
    """Una llamada al modelo, con los parámetros que fija el contrato: temperatura 0."""
    cuerpo = json.dumps({
        "model": MODELO,
        "max_tokens": 16000,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    pedido = urllib.request.Request(API, data=cuerpo, method="POST", headers={
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],   # sale de acá y no vuelve a aparecer
    })
    with urllib.request.urlopen(pedido, timeout=600) as r:
        d = json.loads(r.read().decode("utf-8"))
    partes = [b.get("text", "") for b in d.get("content", []) if b.get("type") == "text"]
    return {
        "texto": "".join(partes),
        "modelo": d.get("model", MODELO),
        "tokens": d.get("usage", {}),
    }


class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)

    def log_message(self, *a):
        pass                                    # sin ruido; y nada de lo que llega se registra

    def _json(self, codigo, dato):
        b = json.dumps(dato, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/api/estado":
            return self._json(200, {"relay": True, "puede_evaluar": hay_key(), "modelo": MODELO})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/evaluar":
            return self._json(404, {"error": "ruta desconocida"})
        if not hay_key():
            return self._json(503, {"error":
                "No hay ANTHROPIC_API_KEY en el entorno de este servidor. Ponela en la terminal "
                "antes de arrancarlo, o segui por copiar y pegar: la consola funciona igual."})
        try:
            largo = int(self.headers.get("content-length", "0"))
            prompt = json.loads(self.rfile.read(largo).decode("utf-8")).get("prompt", "")
        except Exception as e:
            return self._json(400, {"error": "no pude leer el pedido: %s" % e})
        if not prompt.strip():
            return self._json(400, {"error": "el prompt vino vacio"})
        try:
            return self._json(200, evaluar(prompt))
        except urllib.error.HTTPError as e:
            detalle = e.read().decode("utf-8", "replace")[:400]
            return self._json(502, {"error": "el modelo respondio %s: %s" % (e.code, detalle)})
        except Exception as e:
            return self._json(502, {"error": "no pude llamar al modelo: %s" % e})


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("Consola:  http://localhost:%d/front/consola.html" % PUERTO)
    print("Modelo:   %s" % MODELO)
    print("Evaluar:  %s" % ("si, hay key en el entorno" if hay_key()
                            else "no (sin ANTHROPIC_API_KEY). Copiar y pegar sigue andando."))
    try:
        Servidor(("127.0.0.1", PUERTO), Manejador).serve_forever()
    except KeyboardInterrupt:
        print("\nlisto")
        sys.exit(0)
