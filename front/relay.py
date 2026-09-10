# -*- coding: utf-8 -*-
"""Servidor local de la consola: sirve el repositorio y corre el evaluador.

    set ANTHROPIC_API_KEY=...        (Windows, en la misma terminal)
    python front/relay.py

Y despues:  http://localhost:8731/front/consola.html

POR QUE EXISTE Y DONDE ESTA LA LINEA
------------------------------------
La consola no puede llamar al modelo por si sola: hacerlo pediria meter una credencial dentro del
navegador, que es la bandera G8 que esta misma rubrica penaliza. Este archivo mueve la credencial
al unico lugar donde corresponde: el proceso local, leida de una variable de entorno.

- La key nunca entra al navegador, ni al localStorage, ni a un archivo del repositorio.
- No se imprime, no se loguea, no viaja en ninguna respuesta.
- Sin la variable puesta, el relay funciona igual: sirve los archivos y avisa que no puede evaluar.
  El camino de copiar y pegar sigue intacto, y sigue siendo el que anda en cualquier maquina.

Y hace una segunda cosa: bajar el repositorio de una entrega que llego como link. El modelo detras
de la API no navega, asi que si la entrega es una URL el contenido tiene que viajar en el pedido.

Sin dependencias: solo biblioteca estandar.
"""
import http.server
import io as _io
import json
import os
import re
import socketserver
import sys
import urllib.error
import urllib.request
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUERTO = int(os.environ.get("PUERTO", "8731"))
MODELO = os.environ.get("MODELO", "claude-sonnet-5")
API = "https://api.anthropic.com/v1/messages"

EXT_TEXTO = (".md", ".markdown", ".txt", ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg",
             ".csv", ".html", ".htm", ".css", ".js", ".ts", ".py", ".sql", ".sh", ".xml", ".env")
SIN_EXT = ("README", "LICENSE", "MAKEFILE", "DOCKERFILE", "CHANGELOG", "DECISIONES")
TOPE_ARCHIVO = 40000
TOPE_TOTAL = 320000
NL = chr(10)


ARCHIVO_KEY = os.path.join(os.path.expanduser("~"), ".anthropic-key")


def leer_key():
    """La credencial, de la variable de entorno o de un archivo en tu carpeta personal.

    El archivo vive FUERA del repositorio a proposito: en la carpeta del usuario. Asi no se
    puede subir por accidente, que es exactamente la bandera G8 que esta rubrica penaliza.
    Sigue sin entrar al navegador: la lee este proceso y nadie mas.
    """
    k = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if k:
        return k
    # Windows le agrega .txt cuando se guarda desde el Bloc de notas sin cambiar el tipo,
    # y eso ya nos costo una vuelta entera. Se aceptan las dos formas.
    for ruta in (ARCHIVO_KEY, ARCHIVO_KEY + ".txt"):
        try:
            with open(ruta, encoding="utf-8") as f:
                k = f.read().strip().strip('"').strip("'")
            if k:
                return k
        except Exception:
            pass
    return ""


def hay_key():
    return bool(leer_key())


def forma_de_la_key():
    """Describe la credencial SIN revelarla: largo, prefijo y si trae espacios.

    Un 401 puede ser una key vencida o una key bien pegada con un espacio al final. Lo
    segundo se diagnostica mirando la forma, y la forma no es secreta: el prefijo publico
    y la cantidad de caracteres no sirven para autenticarse.
    """
    k = leer_key()
    if not k:
        return {"presente": False}
    return {
        "presente": True,
        "largo": len(k),
        "largo_sin_espacios": len(k.strip()),
        "prefijo": k.strip()[:7],
        "tiene_espacios_alrededor": k != k.strip(),
        "tiene_comillas": k.strip()[:1] in ("'", chr(34)) or k.strip()[-1:] in ("'", chr(34)),
        "tiene_saltos": (chr(10) in k) or (chr(13) in k),
    }


def es_texto(ruta):
    return ruta.lower().endswith(EXT_TEXTO) or os.path.basename(ruta).upper() in SIN_EXT


def bajar_repo(url):
    """Trae un repositorio publico de GitHub y devuelve su arbol y su texto.

    Solo lectura, solo publicos. Lo que no se puede leer se declara en vez de suponerse:
    es la misma regla que el contrato le exige al evaluador en la pasada 1.
    """
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", url.strip())
    if not m:
        raise ValueError("no reconozco la URL como un repositorio de GitHub: " + url)
    duenio = m.group(1)
    repo = m.group(2).replace(".git", "")

    crudo = None
    ultimo = None
    for rama in ("main", "master"):
        try:
            u = "https://codeload.github.com/%s/%s/zip/refs/heads/%s" % (duenio, repo, rama)
            with urllib.request.urlopen(u, timeout=90) as r:
                crudo = r.read()
            break
        except Exception as e:
            ultimo = e
    if crudo is None:
        raise ValueError("no pude bajar el repositorio (%s). Puede ser privado o no existir."
                         % ultimo)

    z = zipfile.ZipFile(_io.BytesIO(crudo))
    arbol = []
    partes = []
    omitidos = []
    total = 0
    for info in z.infolist():
        if info.is_dir():
            continue
        ruta = "/".join(info.filename.split("/")[1:])      # saco la carpeta contenedora
        if not ruta:
            continue
        arbol.append("  %s   (%d bytes)" % (ruta, info.file_size))
        if not es_texto(ruta):
            omitidos.append(ruta + " (binario o no textual)")
            continue
        if total >= TOPE_TOTAL:
            omitidos.append(ruta + " (se llego al tope de lectura)")
            continue
        try:
            txt = z.read(info).decode("utf-8", "replace")
        except Exception as e:
            omitidos.append("%s (no se pudo leer: %s)" % (ruta, e))
            continue
        if len(txt) > TOPE_ARCHIVO:
            txt = txt[:TOPE_ARCHIVO] + NL + "[...recortado, el archivo sigue]"
            omitidos.append(ruta + " (recortado)")
        total += len(txt)
        partes.append("--- %s ---" % ruta + NL + txt)

    return {"archivos": len(arbol),
            "arbol": NL.join(arbol),
            "texto": (NL + NL).join(partes),
            "omitidos": omitidos}


def _llamar(cuerpo):
    pedido = urllib.request.Request(API, data=json.dumps(cuerpo).encode("utf-8"),
                                    method="POST", headers={
        "content-type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": leer_key(),                        # sale de aca y no vuelve a aparecer
    })
    with urllib.request.urlopen(pedido, timeout=900) as r:
        return json.loads(r.read().decode("utf-8"))


def evaluar(prompt):
    """Una llamada al modelo.

    El contrato fija temperatura 0 como primera condicion de determinismo (rubrica.md, 3).
    Los modelos mas nuevos dejaron de aceptar ese parametro: responden 400 diciendo que esta
    deprecado. Se manda igual, y si lo rechazan se reintenta sin el y se declara en la
    respuesta. Preferimos que quede registrado que no se pudo fijar, antes que sacarlo en
    silencio y seguir afirmando temperatura 0 en la firma del informe.
    """
    # Razonamiento extendido APAGADO, y es una decision del contrato, no una optimizacion.
    # Con el prendido, el modelo gasta el presupuesto de salida deliberando y corta el informe
    # a la mitad: 32.000 tokens de salida para 5.259 caracteres de texto, stop_reason max_tokens.
    # Ademas, deliberar distinto en cada corrida es exactamente lo que rubrica.md 3 prohibe.
    base = {"model": MODELO, "max_tokens": int(os.environ.get("MAX_TOKENS", "16000")),
            "thinking": {"type": "disabled"},
            "messages": [{"role": "user", "content": prompt}]}
    temperatura = 0
    intentos = [dict(base, temperature=0), base, {k: v for k, v in base.items() if k != "thinking"}]
    d = None
    ultimo = None
    for i, cuerpo in enumerate(intentos):
        try:
            d = _llamar(cuerpo)
            if i >= 1:
                temperatura = None            # el modelo no acepto fijarla
            break
        except urllib.error.HTTPError as e:
            ultimo = (e, e.read().decode("utf-8", "replace"))
            if e.code != 400:
                break
    if d is None:
        e, detalle = ultimo
        raise urllib.error.HTTPError(e.url, e.code, detalle, e.headers, None)
    partes = [b.get("text", "") for b in d.get("content", []) if b.get("type") == "text"]
    texto = "".join(partes)
    if not texto.strip():
        # El modelo respondio sin texto. Pasa cuando se agota max_tokens antes de escribir,
        # o cuando toda la salida fue de otro tipo de bloque. Hay que decirlo, no devolver
        # una cadena vacia que aguas abajo parece "JSON invalido".
        raise ValueError(
            "el modelo respondio sin texto (stop_reason=%s, bloques=%s, tokens de salida=%s). "
            "Si stop_reason es max_tokens, el informe no entro en el limite." % (
                d.get("stop_reason"),
                [b.get("type") for b in d.get("content", [])],
                d.get("usage", {}).get("output_tokens")))
    return {"texto": texto,
            "modelo": d.get("model", MODELO),
            "temperatura": temperatura,
            "stop_reason": d.get("stop_reason"),
            "tokens": d.get("usage", {})}


class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)

    def log_message(self, *a):
        pass                                # sin ruido, y nada de lo que llega se registra

    def _json(self, codigo, dato):
        b = json.dumps(dato, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _pedido(self):
        largo = int(self.headers.get("content-length", "0"))
        return json.loads(self.rfile.read(largo).decode("utf-8", "replace"))

    def do_GET(self):
        if self.path == "/api/estado":
            return self._json(200, {"relay": True, "puede_evaluar": hay_key(),
                                    "modelo": MODELO, "key": forma_de_la_key()})
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/repo":
            try:
                return self._json(200, bajar_repo(self._pedido().get("url", "")))
            except Exception as e:
                return self._json(502, {"error": str(e)})

        if self.path != "/api/evaluar":
            return self._json(404, {"error": "ruta desconocida"})

        if not hay_key():
            return self._json(503, {"error":
                "No encontre la credencial. Poner la key en " + ARCHIVO_KEY + ", o en la "
                "variable ANTHROPIC_API_KEY antes de arrancar. Sin ella, copiar y pegar funciona igual."})
        try:
            prompt = self._pedido().get("prompt", "")
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
    print("Evaluar:  %s" % ("si, hay credencial" if hay_key()
                            else "NO. Pegar la key en: " + ARCHIVO_KEY))
    if hay_key():
        print("Key:      %d caracteres, empieza con %r" % (len(leer_key()), leer_key()[:7]))
    try:
        Servidor(("127.0.0.1", PUERTO), Manejador).serve_forever()
    except KeyboardInterrupt:
        print("")
        sys.exit(0)
