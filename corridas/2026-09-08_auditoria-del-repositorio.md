# Auditoría del repositorio contra su propio criterio

**Fecha:** 2026-09-08 · **Herramienta:** `auditar.py` · **Contrato:** v1.10

Corregimos trabajos ajenos buscando contradicciones internas, referencias que no resuelven,
aritmética que no cierra y credenciales expuestas. Nunca habíamos hecho eso **con el nuestro**.

```
python auditar.py
```

Ocho bloques: estructura obligatoria, referencias a archivos, referencias a secciones, versiones del
contrato, aritmética de los tres casos, credenciales, los números que el repo afirma sobre sí mismo,
e historia de commits.

---

## Lo que encontró — tres cosas reales, las tres arregladas

### 1 · `calibracion.md` §8 decía «tres cosas» y listaba cuatro

Es exactamente la **G7 — contradicción interna** de nuestra propia rúbrica: *"el trabajo afirma X y
su propia evidencia muestra no-X"*. Es la tercera vez que la encontramos en nuestros documentos
(antes: `rubrica.md (v1.1)` citada cuando el archivo era v1.9, y "ocho vectores… encuentra los
seis" en el README).

Y traía un segundo problema encima: `DECISIONES.md` citaba **§8.1, §8.2, §8.3 y §8.4**, que **no
existían** — eran ítems de una lista numerada, no secciones. Cuatro referencias que no resolvían, en
el documento donde declaramos lo que queda roto.

Arreglado: los cuatro ítems son ahora subsecciones con su título, y las citas resuelven.

### 2 · El caso flojo mostraba la rama que el agente no produce

`casos/flojo/ESPERADO.md` encabezaba su bloque de aritmética con **final 21** (la rama indulgente,
R5.3 = SI) y dejaba la rama severa como una nota entre paréntesis. Pero el agente produce **18**, y
18 es lo que dicen el README, el ensayo de lote y la propia cabecera del archivo.

No estaba *mal* —las dos ramas están documentadas a propósito, porque el caso es ambiguo en R5.3—
pero un lector que abre `ESPERADO.md` veía **21** en la caja. Invertido: ahora encabeza la rama que
el agente efectivamente toma, con la indulgente debajo.

> Vale decir de dónde salió: el auditor no "supo" cuál era la correcta. Sumó las cinco líneas, dio
> **21,25**, y eso no coincidía con el 18 que el repo repite en todos lados. **La contradicción se
> encontró sola**; cuál de los dos números estaba mal lo decidimos nosotros.

### 3 · Un archivo del repositorio que ningún documento nombraba

`PLAN-DE-TRABAJO.md` —el reparto por carriles y la regla de no fabricar la historia de commits— no
figuraba en el mapa del README, y repartía los cuatro carriles entre *"(integrante 1)"*,
*"(integrante 2)"*… mientras el README nombra a las cuatro personas. Un archivo huérfano en la raíz
de un repositorio que se corrige por formato es, como mínimo, ruido. Nombrado en el mapa y con los
carriles a nombre de quien los tiene.

---

## Lo que confirmó que está bien

| Bloque | Resultado |
|--------|-----------|
| **Estructura obligatoria** | Los siete elementos que pide el parcial, presentes |
| **Versiones del contrato** | Los cinco archivos en **1.10**, y el `const` del esquema coincide |
| **Esquema de salida** | 20 propiedades, 20 requeridas, **mismo orden**, `additionalProperties: false` |
| **Aritmética de los casos** | excelente **88,75 → 89** · flojo **17,50 → 18** · tramposo **46,25** · las quince líneas cierran contra los pesos oficiales |
| **Credenciales** | Ninguna real. La única cadena con forma de token es la del caso tramposo, y está declarada como falsa en cuatro archivos |
| **Los cuatro repos ajenos** | Las cuatro corridas existen |

---

## Lo que el auditor no puede encontrar, y es lo más importante

**La historia de commits.** El bloque la mide y no la juzga, porque acá no hay nada mecánico que
arreglar:

```
35 commits, 4 días distintos
   19  Francisco Alloatti
   10  Claude          <- son de Verónica (integración de GitHub; ver README)
    3  Martin99-png
    2  federicobofer
    1  Veropugliese

2026-09-02  ####              4
2026-09-03  ######            6
2026-09-04  ########          8
2026-09-08  #################  17
```

Leído sin piedad: **30 de los 35 commits son de dos personas**, y **17 de 35 son de un solo día**.
El parcial evalúa el proceso grupal con peso 15 y dice que *"un repo con un único commit del último
día cuenta una historia — y no es buena"*. La nuestra no es esa, pero tiene un pico al final que se
ve.

Esto no se arregla editando archivos. Se arregla con lo que ya está pedido en `DECISIONES.md`
—*"Quién tiene qué"*— y sobre todo con la puntuación a ciegas, que **sólo existe si la cargan cuatro
personas distintas**. Y no se arregla, bajo ninguna circunstancia, repartiendo commits: sería usar
el caso tramposo como manual de instrucciones, en el repositorio donde escribimos que eso no se
hace.

**Lo demás que no ve:** si un requisito está *bien pensado*, si una cita sostiene lo que dice
sostener, si un ancla discrimina. Eso lo ve una persona leyendo — o el desacuerdo entre cuatro.

---

## Por qué el auditor no grita

Trece nombres de archivo aparecen citados y no existen en el repositorio, y **está bien que así
sea**: son configuraciones de agente que la rúbrica le enseña a *buscar* dentro del trabajo ajeno
(`GEMINI.md`, `mcp.json`, `.github/copilot-instructions.md`), nombres de ejemplo dentro de las
anclas, y archivos plantados dentro de los casos ficticios.

Cada uno está en una lista **con su motivo escrito**, no silenciado. Es la misma decisión que
tomamos con el vigilante del repositorio cuando marcaba `-----BEGIN PRIVATE KEY-----` dentro de
`agente/banderas.md`, donde es un patrón documentado y no una fuga.

Un auditor con quince falsos positivos no lo corre nadie, y un chequeo que nadie corre es peor que
ninguno: da la sensación de estar cubierto.
