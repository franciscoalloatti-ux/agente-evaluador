# -*- coding: utf-8 -*-
"""Auditoria del repositorio contra su propio criterio.

    python auditar.py

Busca en este repositorio las mismas cosas que el agente busca en los trabajos que
corrige: contradicciones internas, referencias que no resuelven, aritmetica que no
cierra, credenciales, y una historia de commits que no cuente lo que dice contar.
No reemplaza leer: encuentra lo mecanico, que es lo que se nos escapa a nosotros.
Documentado en corridas/2026-09-08_auditoria-del-repositorio.md
"""
import io, os, re, json, subprocess, collections, unicodedata

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

HALLAZGOS = []
def h(sev, cat, msg):
    HALLAZGOS.append((sev, cat, msg))

def leer(p):
    return io.open(p, encoding="utf-8").read()

MDS = []
for base, dirs, files in os.walk("."):
    if ".git" in base: continue
    for f in files:
        MDS.append(os.path.join(base, f).replace("\\", "/")[2:])
TEXTOS = {p: leer(p) for p in MDS if p.endswith((".md", ".json", ".html", ".mjs"))}

print("=" * 72)
print("A · ESTRUCTURA OBLIGATORIA DEL PARCIAL")
print("=" * 72)
exigidos = ["README.md", "rubrica.md", "agente", "casos/excelente", "casos/flojo",
            "casos/tramposo", "calibracion.md"]
for e in exigidos:
    ok = os.path.exists(e)
    print(("  ok   " if ok else "  FALTA") + "  " + e)
    if not ok: h("ALTO", "estructura", "falta " + e)

print()
print("=" * 72)
print("B · REFERENCIAS A ARCHIVOS QUE NO EXISTEN")
print("=" * 72)
pat = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|html|mjs|py|txt))`")
faltantes = collections.defaultdict(list)
for p, t in TEXTOS.items():
    # Un documento que describe un repositorio ajeno cita rutas ajenas. Los casos son trabajos
    # ficticios; las corridas describen el repo que se evaluo, que no es este.
    if p.startswith("casos/") or p.startswith("corridas/"):
        continue
    for m in set(pat.findall(t)):
        cands = [m, os.path.join(os.path.dirname(p), m).replace("\\", "/")]
        if any(os.path.exists(c) for c in cands): continue
        if m.split("/")[-1] in [os.path.basename(x) for x in MDS]: continue
        faltantes[m].append(p)
# Nombres que aparecen citados y NO son archivos de este repo. Cada uno con su motivo:
# si manana alguno deja de tener sentido, hay que sacarlo de aca, no silenciarlo.
ESPERADOS = {
 # configuraciones de agente que la rubrica le ensena a BUSCAR dentro del trabajo evaluado (G3d)
 "GEMINI.md": "config de agente que el evaluador busca en el repo ajeno",
 "mcp.json": "idem",
 ".github/copilot-instructions.md": "idem",
 ".vscode/settings.json": "idem",
 # nombres de ejemplo dentro de las anclas de la rubrica: describen un trabajo imaginario
 "corridas/2026-09-05-1.md": "ancla de nivel 4 de D1: nombre de ejemplo",
 "corridas/2026-09-04_remito-1183.md": "ancla de nivel 4 de D3: nombre de ejemplo",
 "..._remito-1207.md": "idem", "..._remito-1219.md": "idem",
 "ejemplo.txt": "ancla de nivel 1 de D3: nombre de ejemplo",
 # archivos plantados DENTRO de los casos ficticios, o citados por ellos
 "criterios-oficiales.md": "archivo plantado que banderas.md usa de ejemplo de G3b",
 "feedback-catedra.md": "idem, ejemplo de G3c",
 "notas.txt": "idem", "prompts/notas.txt": "idem",
 "corridas/log_api.txt": "archivo del caso tramposo v1, archivado",
 # archivos que viven DENTRO de caso-06.zip, el trabajo ajeno que mando el profesor el 10/9.
 # Los citamos porque de ahi salio la regla de la mencion; no son archivos nuestros.
 "docs/seguridad.md": "esta dentro de caso-06.zip (el trabajo ajeno), no en este repo",
 "datos/correo_02.json": "idem", "datos/correo_03.json": "idem",
 "proceso/ajuste_citas.md": "idem",
 "src/main.py": "idem: el codigo de caso-02.zip, citado por la regla de G2",
}
GENERICOS = {"system_prompt.md", "user_prompt.md", "DECISIONES.md", "README.md",
             "esquema_salida.json", "rubrica.md", "banderas.md", "config.md",
             "ESPERADO.md", "lote.md", "calibracion.md", "plantilla_informe.md",
             "AGENTS.md", "CLAUDE.md", "docs/rubrica-catedra.md", "docs/devolucion-previa.md",
             "consola.html", "probar.mjs", "rubrica-catedra.md", "devolucion-previa.md",
             "MEMORY.md", "hosts.yml", ".cursorrules"}
rotas = 0
for m, quien in sorted(faltantes.items()):
    if m in GENERICOS or m.split("/")[-1] in GENERICOS: continue
    if m in ESPERADOS:
        print("  ok     " + m.ljust(38) + ESPERADOS[m]); continue
    print("  ROTA   " + m + "   citada en: " + ", ".join(sorted(set(quien))))
    h("MEDIO", "referencia", m + " no existe (citada en " + ", ".join(sorted(set(quien))) + ")")
    rotas += 1
if not rotas: print("  ok     ninguna referencia rota")

print()
print("=" * 72)
print("C · REFERENCIAS A SECCIONES (§) QUE NO EXISTEN")
print("=" * 72)
sec = re.compile(r"`([A-Za-z0-9_./-]+\.md)`\s*§\s*([0-9]+(?:\.[0-9]+)?(?:\s*bis)?)")
malas = 0
for p, t in TEXTOS.items():
    if p.startswith("casos/"): continue
    for arch, num in set(sec.findall(t)):
        cands = [arch, os.path.join(os.path.dirname(p), arch).replace("\\", "/")]
        destino = next((c for c in cands if os.path.exists(c)), None)
        if not destino:
            destino = next((x for x in MDS if x.endswith("/" + arch) or x == arch), None)
        if not destino: continue
        d = leer(destino)
        num_l = num.replace(" ", " ").strip()
        if re.search(r"^#{2,4}\s*" + re.escape(num_l) + r"\b", d, re.M) or \
           re.search(r"^#{2,4}\s*" + re.escape(num_l) + r"\s*[·.]", d, re.M):
            continue
        print("  ROTA   " + arch + " §" + num + "   citada en " + p)
        h("MEDIO", "referencia", arch + " §" + num + " no existe (citada en " + p + ")")
        malas += 1
if not malas: print("  ok   todas las secciones citadas existen")

print()
print("=" * 72)
print("D · VERSIONES DEL CONTRATO")
print("=" * 72)
def ver(t):
    m = re.search(r"Versi[oó]n\s+\**\s*(\d+\.\d+)", t) or re.search(r'"version"\s*:\s*"([\d.]+)"', t)
    return m.group(1) if m else None
contrato = ["rubrica.md", "agente/system_prompt.md", "agente/banderas.md",
            "agente/esquema_salida.json", "agente/config.md"]
vs = {}
for c in contrato:
    vs[c] = ver(leer(c)); print("  " + str(vs[c]).ljust(6) + " " + c)
distintas = set(v for v in vs.values() if v)
if len(distintas) > 1:
    h("ALTO", "coherencia", "el contrato tiene versiones distintas: " + " · ".join(sorted(distintas)))
    print("  DESACUERDO entre archivos del contrato")
else:
    print("  ok   las cinco coinciden")
esq = json.loads(leer("agente/esquema_salida.json"))
const = esq["properties"]["version_rubrica"].get("const")
print("  version_rubrica const = " + str(const) + ("   ok" if const in distintas else "   NO COINCIDE"))
if const not in distintas:
    h("ALTO", "coherencia", "el esquema exige version_rubrica " + str(const) + " y la rubrica es " + str(list(distintas)))

print()
print("=" * 72)
print("E · ARITMETICA DE LOS CASOS (ESPERADO.md)")
print("=" * 72)
lin = re.compile(r"^(D[1-5])\s+(\d)/4\s*[x\*]\s*(\d+)\s*=\s*([\d.,]+)", re.M)
PESOS = {"D1": 30, "D2": 25, "D3": 15, "D4": 15, "D5": 15}
for caso in ["excelente", "flojo", "tramposo"]:
    f = "casos/" + caso + "/ESPERADO.md"
    if not os.path.exists(f): continue
    t = leer(f); filas = lin.findall(t)
    if not filas:
        print("  " + caso + ": sin lineas de calculo legibles"); continue
    total = 0.0; err = []
    for dim, niv, peso, res in filas:
        esperado = (int(niv) / 4) * int(peso)
        dado = float(res.replace(".", "").replace(",", "."))
        total += esperado
        if int(peso) != PESOS[dim]: err.append(dim + " usa peso " + peso + ", el oficial es " + str(PESOS[dim]))
        if abs(esperado - dado) > 0.01: err.append(dim + ": " + niv + "/4 x " + peso + " = " + ("%.2f" % esperado) + ", dice " + res)
    print("  " + caso.ljust(10) + " suma de dimensiones = " + ("%.2f" % total))
    for e in err:
        print("     ERROR  " + e); h("ALTO", "aritmetica", caso + ": " + e)
    if not err: print("     ok   las cinco lineas cierran")

print()
print("=" * 72)
print("F · CREDENCIALES")
print("=" * 72)
PAT = [(r"sk-[A-Za-z0-9]{20,}", "clave estilo OpenAI"),
       (r"ghp_[A-Za-z0-9]{30,}", "token de GitHub"),
       (r"AKIA[0-9A-Z]{16}", "clave de AWS"),
       (r"bnk_live_[a-f0-9]{20,}", "credencial del caso tramposo"),
       (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "clave privada")]
DOC = {"agente/banderas.md", "rubrica.md", "agente/system_prompt.md", "README.md"}
for p, t in TEXTOS.items():
    for rx, nom in PAT:
        for m in set(re.findall(rx, t)):
            esperado = (p.startswith("casos/tramposo") or p.startswith("corridas/")
                        or p in DOC or p == "casos/README.md")
            marca = "  ok   " if esperado else "  ALERTA"
            print(marca + "  " + nom + " en " + p)
            if not esperado:
                h("ALTO", "seguridad", nom + " en " + p)

print()
print("=" * 72)
print("G · NUMEROS QUE EL REPO AFIRMA SOBRE SI MISMO")
print("=" * 72)
rub = leer("rubrica.md")
reales = {
  "requisitos verificables (R*.*)": len(set(re.findall(r"\bR[1-5]\.[1-4]\b", rub))),
  "banderas (G*)":                  len(set(re.findall(r"\bG[1-8][a-d]?\b", rub))),
  "estados":                        len(re.findall(r"^\| `(evaluado|evaluado_con_reservas|integridad_comprometida|fuera_de_alcance|no_evaluable)`", rub, re.M)),
  "archivos en corridas/":          len(os.listdir("corridas")),
  "chequeos de auditoria (A*)":     len(set(re.findall(r"\bA[1-9]\b", leer("agente/system_prompt.md")))),
  "cruces (C*)":                    len(set(re.findall(r"\bC[1-7]\b", leer("agente/system_prompt.md")))),
  "vectores G3 del tramposo":       len(re.findall(r"^\| \d+ \| \*\*G3", leer("casos/tramposo/ESPERADO.md"), re.M)),
}
for k, v in reales.items(): print("  " + str(v).rjust(3) + "  " + k)

PALABRAS = {"cinco":5,"seis":6,"siete":7,"ocho":8,"nueve":9,"diez":10,"once":11,"doce":12,
            "trece":13,"catorce":14,"quince":15,"dieciséis":16,"veinte":20,
            "treinta y tres":33,"cuatro":4,"tres":3}
print()
print("  afirmaciones numericas en README.md:")
rd = leer("README.md")
for frase, n in [("veinte requisitos", 20), ("once banderas", 11), ("ocho vectores", 8),
                 ("los ocho", 8), ("Diecisiete informes", 17), ("cinco dimensiones", 5)]:
    if frase.lower() in rd.lower():
        print("     dice '" + frase + "'")

print()
print("=" * 72)
print("H · HISTORIA DE COMMITS (15% de la nota del parcial)")
print("=" * 72)
def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, encoding="utf-8").stdout
log = git("log", "--format=%an|%ad", "--date=short").strip().split("\n")
autores = collections.Counter(l.split("|")[0] for l in log if l)
dias = collections.Counter(l.split("|")[1] for l in log if l)
print("  " + str(len(log)) + " commits, " + str(len(dias)) + " dias distintos")
for a, n in autores.most_common(): print("     " + str(n).rjust(3) + "  " + a)
print("  por dia:")
for d, n in sorted(dias.items()): print("     " + d + "  " + ("#" * n) + " " + str(n))
if len(dias) < 3:
    h("ALTO", "proceso", "la historia se concentra en menos de 3 dias")

# El conteo de corridas quedo viejo tres veces (16 -> 17 -> 19). Que lo controle la maquina.
NUM = {"cinco":5,"seis":6,"siete":7,"ocho":8,"nueve":9,"diez":10,"once":11,"doce":12,"trece":13,
       "catorce":14,"quince":15,"dieciseis":16,"diecisiete":17,"dieciocho":18,"diecinueve":19,
       "veinte":20,"veintiuno":21,"veintiun":21,"veintidos":22,"veintidos":22,"veintitres":23,"veintidos":22,"veintitres":23,"veinticuatro":24,"veinticinco":25,"veintiseis":26,"veintisiete":27,"veintiocho":28,
       "veintinueve":29,"treinta":30}
rd_ = leer("README.md")
m_ = re.search(r"(\w+) informes y ensayos guardados en `corridas/`", rd_)
real_ = len(os.listdir("corridas"))
if m_:
    sinac_ = ''.join(c for c in unicodedata.normalize('NFD', m_.group(1))
                     if unicodedata.category(c) != 'Mn').lower()
    dicho_ = NUM.get(sinac_)
    if dicho_ == real_:
        print("  ok     el README dice '" + m_.group(1) + "' y hay " + str(real_) + " corridas")
    else:
        print("  ERROR  el README dice '" + m_.group(1) + "' y hay " + str(real_) + " corridas")
        h("MEDIO", "coherencia", "el README declara " + str(dicho_) + " informes en corridas/ y hay " + str(real_))
else:
    print("  aviso  no encontre la frase del conteo de corridas en el README")

print()
print("=" * 72)
print("I · COMMITS CITADOS EN LOS DOCUMENTOS")
print("=" * 72)
citados = set()
for p_, t in TEXTOS.items():
    if not p_.endswith(".md"): continue
    for m in re.findall(r"`([0-9a-f]{7,10})`", t):
        citados.add((m, p_))
if not citados:
    print("  ningún documento cita un commit")
for h_, donde in sorted(citados):
    vivo = subprocess.run(["git","merge-base","--is-ancestor",h_,"HEAD"],
                          capture_output=True).returncode == 0
    print(("  ok     " if vivo else "  ROTA   ") + h_ + "   " + donde)
    if not vivo:
        h("ALTO", "referencia", "el commit " + h_ + " citado en " + donde + " no existe en esta "
          "historia (¿se reescribió con un force-push?)")

print()
print("=" * 72)
print("RESUMEN")
print("=" * 72)
if not HALLAZGOS:
    print("  sin hallazgos automaticos")
for sev, cat, msg in HALLAZGOS:
    print("  [" + sev + "] " + cat + ": " + msg)
print("  total: " + str(len(HALLAZGOS)))
