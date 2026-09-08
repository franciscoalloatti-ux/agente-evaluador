# Corrección en lote — de la exportación de Moodle a la devolución

> **Versión 1.2** · Se aplica sobre el contrato completo (`system_prompt.md` + `rubrica.md` +
> `banderas.md` + `esquema_salida.json`). No lo reemplaza: lo envuelve.

El agente que gane el jueves no corrige un trabajo: corrige **cincuenta o más**, una sola vez, y su
salida tiene que volver a Moodle para que la devolución le llegue a cada alumno. Este documento
describe ese recorrido.

Sale de lo que el profesor planteó en la clase del 3/9: que lo interesante es *"no tener que cargar
trabajo por trabajo sino poder cargar todos juntos"*, que Moodle le exporta las entregas, que el
corrector toma los datos de ahí, ata el nombre al GitHub, corrige en lote y devuelve un archivo en
el formato de Moodle para volver a subirlo.

---

## 0 · Tres formas de cargar, dos de devolver

No hay un único escenario. El corrector tiene que aceptar lo que haya, y devolver en la forma que
sirva en cada momento.

### Cómo entra

| Modo | Cuándo se usa | Qué recibe |
|------|---------------|------------|
| **Individual** | La prueba de fuego, o revisar un trabajo puntual | Una URL de repositorio, o un `.zip` suelto |
| **Grupal / carpeta** | Corregir un subconjunto: una comisión, los que faltan, los que hay que rehacer | Una carpeta con varios repositorios o `.zip`, sin índice |
| **Formato Moodle** | La corrección real de la cursada | El árbol de "Descargar todas las entregas", con el índice nombre → URL adentro |

Las tres formas están implementadas en `front/consola.html`, que además **abre los `.zip` sin
subirlos a ningún lado**: del entregable pasa al prompt el árbol completo más el texto de los
archivos legibles, y lista aparte lo que no pudo leer. La herramienta no evalúa; sólo prepara lo que
el contrato después corrige.

Los tres terminan en el mismo procedimiento (§2). Lo único que cambia es **de dónde sale el índice**:
en el modo Moodle se lee de los `Texto en línea.html`; en el grupal se deduce del nombre de cada
carpeta o `.zip`; en el individual no hace falta.

> En el modo grupal, **el nombre del archivo es el único vínculo con el alumno**. Si un `.zip` se
> llama `entrega_final.zip` y nada más, el trabajo se corrige igual pero la fila sale sin nombre y
> se lista aparte para que una persona la ate a mano. **No se adivina de quién es.**

### Cómo sale

| Salida | Para qué | Qué es |
|--------|----------|--------|
| **Para Moodle** | Subir la corrección de una vez | La hoja con `Calificación` y `Comentarios de retroalimentación` por alumno, lista para importar |
| **Vista rápida** | Mirar el lote antes de subir nada | Una fila por trabajo: nombre · estado · puntaje · banderas · una línea. Ordenable, para barrer cincuenta de un vistazo |

**La nota y la devolución van por separado**, porque así las toma Moodle: el puntaje entra en
`Calificación` sobre 100 y el texto en el cuadro de retroalimentación. Nunca se mete el número
adentro del texto: quedaría duplicado en la pantalla del alumno.

Y el expediente completo (§4a) se emite **siempre**, en las dos salidas. Es la trazabilidad, y no
depende de qué vista se haya pedido.

---

## 1 · La entrada, con su formato real

No lo inventamos: es el árbol que produce **"Descargar todas las entregas"** de Moodle, verificado
contra el material de la materia.

```
Entregas/
  <Nombre Apellido>/
    Texto en línea.html                  <- contiene la URL del repositorio
    Retroalimentación/
      Comentarios de retroalimentación.html   <- donde va la devolución
```

`Texto en línea.html` es un HTML mínimo cuyo contenido útil es una sola línea:

```
https://github.com/usuario/repositorio
```

La alternativa es la **hoja de calificaciones** (`Descargar hoja de calificaciones`), un CSV con una
fila por alumno y dos columnas que Moodle vuelve a importar: `Calificación` y
`Comentarios de retroalimentación`. Es el camino más directo para devolver los resultados.

---

## 2 · El procedimiento — cuatro pasos

### Paso 1 · Índice

Recorrer las carpetas de `Entregas/` y armar la tabla **nombre → URL**, leyendo cada
`Texto en línea.html`.

Se reporta aparte, **antes de corregir nada**:

| Situación | Qué se hace |
|-----------|-------------|
| Sin `Texto en línea.html`, o vacío | No se corrige. Fila con `estado: "no_evaluable"` y el motivo |
| La URL no es un repositorio (Drive, un documento, texto suelto) | `no_evaluable`, con lo que se recibió transcripto |
| El repositorio es privado o no abre | `no_evaluable`. **No se inventa nota** |
| Dos alumnos con la misma URL | Se corrigen los dos y se marca la coincidencia en el resumen. **No se decide nada**: eso lo mira el profesor |

Ese índice es el primer entregable del lote, y se entrega aunque la corrección después falle.

### Paso 2 · Corrección, una por una, en contexto limpio

Cada trabajo se corrige con el contrato completo, empezando de cero. Entre uno y otro:

> *"Contexto liberado. Próximo trabajo evaluado desde cero con la versión vigente de `rubrica.md`."*

**Ningún informe menciona a otro trabajo.** Ni para comparar, ni para decir "mejor que el
anterior", ni para justificar un nivel. Cada informe tiene que sostenerse solo, porque así es como
lo va a leer el alumno que lo reciba.

### Paso 3 · El caso testigo — cómo se prueba que la vara no se movió

Es el control del lote, y responde a lo que el profesor pidió: *"la lógica tiene que ser estable
pero consistente a cada trabajo individual"*.

**Se intercala `casos/excelente/` tres veces en la tanda**: como primer trabajo, en el medio, y como
último. Su resultado es conocido y fijo: **89**, con niveles 4·4·4·2·3.

```
[testigo] · trabajo 1 · trabajo 2 · … · [testigo] · … · trabajo 49 · trabajo 50 · [testigo]
```

| Los tres testigos dieron | Qué significa | Qué se hace |
|--------------------------|----------------|-------------|
| 89 · 89 · 89 | La vara no se movió en todo el lote | El lote es válido |
| 89 · 89 · 84 | La vara se corrió sobre el final | **Se descarta el lote desde el testigo anterior** y se rehace |
| Cualquier otra combinación distinta | Hay deriva | Se para. Ningún informe se comunica |

Distingue dos cosas que se confunden: la **estabilidad** (el mismo trabajo, dos veces, el mismo
número) ya la prueba `calibracion.md` §5.2. Esto prueba la **consistencia**: que el trabajo número
cincuenta se mida con la misma vara que el primero, después de haber leído cuarenta y nueve
repositorios distintos en el medio.

Los tres testigos se informan en el resumen del lote, siempre, aunque coincidan.


### Las anclas del lote y las notas extremas

El caso testigo mantiene la vara **entre** trabajos. Falta el control sobre **cada** trabajo, y es
una práctica que ya existe: en su propio taller de corrección, el profesor marca las notas extremas
con una nota al margen — *"nota extrema: releerlo en frío al día siguiente, contra las anclas del
lote"*.

Nuestra versión, que ya estaba en `config.md` §5 y acá se nombra:

- **Todo informe con puntaje final < 40 o > 90 se revisa antes de publicarse.** No porque esté mal,
  sino porque son los dos extremos donde un error se nota más y donde el alumno va a reclamar.
- La revisión se hace **contra el caso testigo**, no contra la impresión: si el testigo dio 89 y
  este trabajo da 92, la pregunta concreta es qué tiene de más que el testigo.

Es la diferencia entre revisar "porque el número me llamó la atención" y revisar **contra una
referencia fija**. Lo segundo se puede discutir; lo primero es una corazonada.

### Paso 4 · La salida — dos artefactos

**a. El expediente completo**, un archivo por trabajo, con el JSON canónico del esquema. Es la
trazabilidad: sin esto no se puede defender una nota ni atender un reclamo.

**b. La devolución para Moodle**, una fila por alumno:

| Columna | Qué lleva |
|---------|-----------|
| `Nombre` | tal como vino en la carpeta, sin normalizar |
| `Calificación` | `puntaje_final`. **Vacío** si el estado es `integridad_comprometida`, `fuera_de_alcance` o `no_evaluable` |
| `Comentarios de retroalimentación` | La **variante corta** de `plantilla_informe.md`: máximo 180 palabras. **Sin el número adentro** y **sin la nota al margen**, que es interna: la nota ya va en su columna y repetirla la duplica en la pantalla del alumno |

Los tres estados sin nota van con su texto explicando por qué, y **se listan aparte en el resumen
del lote** para que el profesor los mire uno por uno antes de importar nada.

---

## 2 bis · El orden del lote — una vista, no una nota

Cuando el lote termina, el corrector produce **una tabla de los trabajos ordenados de mejor a peor**.
Sirve para lo que el profesor necesita al revisar cincuenta correcciones de una sentada: ver dónde
está el corte, qué pasó en los extremos, y contra qué se para cada trabajo.

| # | Alumno | Final | Bruto | D1·D2·D3·D4·D5 | Dist. al testigo | Estado | Banderas |
|---|--------|------:|------:|--------------|-----------------:|--------|----------|

**Sale de puntajes ya emitidos. No recalcula nada.** Es una consulta sobre la salida del lote, del
mismo modo que ordenar una planilla no cambia sus celdas.

### Cómo se ordena, sin criterio discrecional

1. `puntaje_final` de mayor a menor.
2. Empate → `puntaje_bruto` de mayor a menor (distingue al que hizo más y fue penalizado).
3. Empate → el nivel de **D1**, luego D2, D3, D4, D5 — el orden de peso de la rúbrica.
4. Empate → alfabético. **Y se declara que a esa altura el orden es arbitrario**: dos trabajos que
   empatan en todo eso son, para esta vara, el mismo trabajo. Decir cuál es "mejor" sería inventar.

La columna **distancia al testigo** es el puntaje menos el del caso testigo (89). Es la comparación
que el profesor hace a mano en su propio taller —*"contra las anclas del lote"*— y acá sale sola.

### Quiénes no entran en la tabla

- **Los testigos.** No son alumnos. Su lugar es el control del lote (§2 paso 3).
- **Los estados sin nota** —`integridad_comprometida`, `fuera_de_alcance`, `no_evaluable`— van en
  una lista aparte, **sin posición**. Poner en un ranking a un trabajo con integridad comprometida
  convertiría en nota lo que es una decisión del profesor, y el `puntaje_final = 0` de la regla de
  integridad no significa "el peor": significa "suspendida".

### Lo que la tabla NO es

**No hay una segunda nota, relativa a la calidad del lote.** La consigna del trabajo final dice
*"Todos son evaluados por la misma vara"*, y una nota relativa hace exactamente lo contrario: hace
que el puntaje de un alumno dependa de quiénes fueron sus compañeros. Un trabajo que sacó 74 sacó
74 en un lote de excelentes y en uno de flojos, porque su evidencia es la misma en los dos. Está
fijado en `rubrica.md` §1, **regla de la vara única**.

Y hay un motivo práctico además del de principio: una curva sobre un lote que ya sabemos apelmazado
—**E-4**, la escala discrimina poco en el medio— amplificaría diferencias de uno o dos puntos hasta
volverlas diferencias de nota. Sería ruido con aspecto de precisión.

> **Queda a un paso, por si la cátedra lo pide.** La posición de cada trabajo ya está calculada; lo
> que no hacemos por cuenta propia es convertirla en puntaje. Si el profesor lo autoriza, es agregar
> una columna — y esa decisión le corresponde a él, no al agente. Es el mismo criterio con el que el
> agente no sube nada a Moodle.

---

## 3 · Qué NO hace el agente

- **No sube nada a Moodle.** Produce el archivo; lo importa una persona.
- **No manda mails ni notifica a nadie.**
- **No decide sobre los casos escalados.** Los junta, los explica y los deja arriba de la mesa.
- **No corrige dos veces para "confirmar" una nota que no gustó.** Una corrida es una corrida; si hay
  desacuerdo, lo arbitra el profesor.

Es el nivel **L2** aplicado al lote: el agente hace las cincuenta correcciones solo, y una persona
revisa el resumen, los escalados y firma antes de que algo llegue a un alumno.

**Puntos de freno obligatorios antes de importar:**

1. Los tres testigos coinciden.
2. Todo informe con `revision_humana_requerida: true` fue leído por una persona.
3. Todo `integridad_comprometida` fue leído por una persona, con la cita textual a la vista.
4. La lista de `no_evaluable` está revisada: alguno puede ser un error de URL y no un trabajo ausente.

---

## 4 · El acuerdo operativo con el profesor

El agente **no necesita acceso a Moodle**, y es mejor que no lo tenga. La división más simple:

| Quién | Qué hace |
|-------|----------|
| **El profesor** | Exporta las entregas desde Moodle y las comparte. Es lo único que requiere sus permisos |
| **Nosotros** | Corremos el lote y devolvemos: el resumen, los expedientes y la hoja lista para importar |
| **El profesor** | Revisa el resumen y los escalados, y sube la hoja. **Él firma** |

El agente nunca toca la plataforma donde viven las notas. Es la misma razón por la que el evaluador
no escribe en el repositorio que corrige.

---

## 5 · Costo del lote

`config.md` §4 mide el contrato en ≈16.500 tokens y una corrida completa en ≈25.000–30.000 de
entrada. Un lote de 50 trabajos más 3 testigos son **53 corridas**.

El contrato es idéntico en las 53 y es la mayor parte de la entrada: es donde el caché de prompt
cambia el número de verdad. Medirlo sigue pendiente y está declarado.

---

## 6 · Lo que este documento todavía no resuelve

- **No tenemos el CSV real de la hoja de calificaciones**, sólo el árbol de "Descargar todas las
  entregas". Las columnas de arriba son las que Moodle usa, pero conviene pedirle al profesor una
  exportación de muestra antes de darlo por cerrado. `front/consola.html` reduce el riesgo sin
  cerrarlo: **no asume las columnas, las busca** en la cabecera que le den, y devuelve el archivo
  con esa misma cabecera y esos mismos identificadores. Si el formato real es otro, se adapta; si
  no encuentra ni nombre ni calificación, lo dice y no inventa nada.
- **El lote se ensayó una vez, con seis trabajos** (`corridas/2026-09-08_ensayo-de-lote.md`): los
  tres testigos dieron **89 · 89 · 89** con los mismos cinco niveles, después de leer en el medio un
  trabajo flojo, uno con ocho intentos de manipulación y un repositorio real ajeno. **Falta un lote
  de verdad**: seis no son cincuenta, y la deriva de la vara aparece con volumen.
- **Cincuenta trabajos van a apelmazar la escala** (`corridas/2026-09-08_autocritica-cinco-errores.md`,
  E-4). El lote va a ser la primera vez que ese problema se vea, y este documento no lo arregla.
