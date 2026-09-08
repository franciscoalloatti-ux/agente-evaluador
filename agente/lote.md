# Corrección en lote — de la exportación de Moodle a la devolución

> **Versión 1.0** · Se aplica sobre el contrato completo (`system_prompt.md` + `rubrica.md` +
> `banderas.md` + `esquema_salida.json`). No lo reemplaza: lo envuelve.

El agente que gane el jueves no corrige un trabajo: corrige **cincuenta o más**, una sola vez, y su
salida tiene que volver a Moodle para que la devolución le llegue a cada alumno. Este documento
describe ese recorrido.

Sale de lo que el profesor planteó en la clase del 3/9: que lo interesante es *"no tener que cargar
trabajo por trabajo sino poder cargar todos juntos"*, que Moodle le exporta las entregas, que el
corrector toma los datos de ahí, ata el nombre al GitHub, corrige en lote y devuelve un archivo en
el formato de Moodle para volver a subirlo.

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

> *"Contexto liberado. Próximo trabajo evaluado desde cero con `rubrica.md` v1.8."*

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

### Paso 4 · La salida — dos artefactos

**a. El expediente completo**, un archivo por trabajo, con el JSON canónico del esquema. Es la
trazabilidad: sin esto no se puede defender una nota ni atender un reclamo.

**b. La devolución para Moodle**, una fila por alumno:

| Columna | Qué lleva |
|---------|-----------|
| `Nombre` | tal como vino en la carpeta, sin normalizar |
| `Calificación` | `puntaje_final`. **Vacío** si el estado es `integridad_comprometida`, `fuera_de_alcance` o `no_evaluable` |
| `Comentarios de retroalimentación` | La **variante corta** de `plantilla_informe.md`: máximo 180 palabras |

Los tres estados sin nota van con su texto explicando por qué, y **se listan aparte en el resumen
del lote** para que el profesor los mire uno por uno antes de importar nada.

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
  exportación de muestra antes de darlo por cerrado.
- **Nunca corrimos un lote.** El caso testigo está diseñado y no probado: hace falta una tanda de
  al menos cinco repositorios reales con los tres testigos intercalados. Es el ensayo que sigue.
- **Cincuenta trabajos van a apelmazar la escala** (`corridas/2026-09-08_autocritica-cinco-errores.md`,
  E-4). El lote va a ser la primera vez que ese problema se vea, y este documento no lo arregla.
