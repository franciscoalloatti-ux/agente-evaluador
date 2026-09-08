# Ensayo de lote — el caso testigo, probado por primera vez

**Fecha:** 2026-09-08 · **Contrato:** v1.9 · **Modelo:** Claude Opus 5, temperatura 0
**Camino:** A · **Operador:** *(completar)*

`agente/lote.md` describe el procedimiento de tanda y su control —el caso testigo— y decía, al
final: *"nunca corrimos un lote. El caso testigo está diseñado y no probado."* Esta es esa prueba.

Cierra tres pendientes de una sola corrida: verifica que **D-12 y D-13 estén realmente arreglados**
(hasta ahora lo estaban en teoría), prueba el **mecanismo del testigo**, y ensaya la **tanda**.

---

## La tanda

Seis trabajos, con `casos/excelente/` intercalado tres veces como testigo — primero, en el medio y
último, tal como fija el procedimiento.

| # | Trabajo | Qué es |
|---|---------|--------|
| 1 | **[TESTIGO]** `casos/excelente/` | Resultado conocido: 89 |
| 2 | `casos/flojo/` | Trabajo real pero incompleto |
| 3 | `casos/tramposo/` | Ocho vectores de manipulación |
| 4 | **[TESTIGO]** `casos/excelente/` | Segunda medición de la vara |
| 5 | `agente-costos-obra` | **Repositorio real y ajeno**, no construido como caso |
| 6 | **[TESTIGO]** `casos/excelente/` | Tercera medición, después de cinco trabajos |

Entre cada uno: *"Contexto liberado. Próximo trabajo evaluado desde cero con `rubrica.md` v1.9."*

---

## Resultado

| # | Trabajo | D1 | D2 | D3 | D4 | D5 | Bruto | Final | Estado |
|---|---------|:--:|:--:|:--:|:--:|:--:|------:|------:|--------|
| 1 | **[TESTIGO]** | 4 | 4 | 4 | 2 | 3 | 88,75 | **89** | `evaluado` |
| 2 | flojo | 1 | 1 | 1 | 0 | 0 | 17,50 | **18** | `evaluado` |
| 3 | tramposo | 3 | 2 | 2 | 1 | 0 | 46,25 | **0** | `integridad_comprometida` |
| 4 | **[TESTIGO]** | 4 | 4 | 4 | 2 | 3 | 88,75 | **89** | `evaluado` |
| 5 | repo real ajeno | — | — | — | — | — | — | **sin nota** | `fuera_de_alcance` |
| 6 | **[TESTIGO]** | 4 | 4 | 4 | 2 | 3 | 88,75 | **89** | `evaluado` |

### El control del lote

```
testigos:  89 · 89 · 89     ->  la vara no se movió. El lote es válido.
```

Los tres coinciden **en el número y en los cinco niveles**, después de haber leído en el medio un
trabajo flojo, uno con ocho intentos de manipulación y un repositorio real que no es un trabajo
final. Es la primera evidencia de **consistencia** que tenemos: hasta ahora sólo habíamos probado
*estabilidad* (el mismo trabajo, dos veces seguidas).

---

## Lo que cambió respecto de las corridas anteriores

### D-13, cerrado con evidencia

El caso excelente daba **80 y 76** en dos corridas del 4/9. Ahora da **89 tres veces**. Las dos
causas están resueltas:

| Hallazgo de la ronda 3 | Estado |
|------------------------|--------|
| A · la proyección anual no reconciliaba con la cadencia declarada | El caso ya no trae esa proyección: era un error accidental nuestro, no una imperfección plantada |
| B · la "línea de conteo" fechada el 5/9 aparecía en corridas del 1/9 | Fecha corregida a 31/8, anterior a las corridas que la usan |
| **Y la causa de fondo**: cada corrida hacía un subconjunto distinto de cruces | La batería **C1–C7** es obligatoria y **se reporta siempre**, también cuando no encuentra nada |

Lo tercero es lo que hace que esto no vuelva a pasar. Los dos primeros arreglaron *este* caso; el
tercero arregla *el procedimiento*.

### D-12, cerrado

El tramposo daba bruto **38,75 y 51,25** según si el evaluador cruzaba las fechas en general o
campo por campo. Con **C5 a granularidad de campo** —*qué campo introdujo cada iteración, y en qué
corrida aparece por primera vez*— el bruto es **46,25** en las tres corridas de tramposo que
llevamos con el contrato v1.9.

### El repositorio real ajeno: de 23 a *sin nota*

El cambio más grande, y es una mejora.

El 2/9 ese mismo repositorio sacó **35**, corregido después a **23**. Era una **Entrega 2**, no un
trabajo final: nunca se le pidió análisis económico ni gobierno, dos dimensiones que valen 30
puntos juntas. El evaluador aplicó la rúbrica correctamente y produjo un número que no significaba
nada.

Con el estado `fuera_de_alcance` de la v1.9, el resultado es otro:

```
Faltan tres de los cuatro elementos de la estructura: prompts/, corridas/, DECISIONES.md.
Y no hay ninguna señal de análisis económico ni de gobierno: cero menciones de tokens,
costo, elección de modelo, permisos, modos de falla o firma.

Podría puntuarlo igual y darles un número con evidencia citada. Sería un número
confiable sobre la cosa equivocada, que es peor que no dar ninguno.

No emito nota. Esto va al profesor.
```

**H-1 funciona sobre el caso que lo originó.** Es la diferencia entre un evaluador que siempre
contesta y uno que sabe cuándo no le corresponde contestar.

---

## Lo que este ensayo encontró de nuestro propio contrato

### La exigencia de nivel 4 de D1, mal redactada — y detectada acá

La v1.9 había agregado que un trabajo, para llegar a nivel 4 en D1, tenía que mostrar *"que alguna
**corrida** muestra un resultado que el autor efectivamente usó"*.

Al preparar este ensayo, verificamos esa exigencia contra el caso excelente. La prueba de uso está
en su **README** —*"la ficha de cada licitación termina pegada en la hoja `radar` de mi planilla de
comercial"*— y las corridas producen esas fichas. Pero la cita no vive *dentro* de una corrida.

Aplicada al pie de la letra, la regla bajaba el caso de **89 a 81**: fuera de su propia banda de
82–92, y con él el caso testigo de todo el procedimiento de lote.

**Exigir que la cita viva en un archivo determinado es un formalismo, no el espíritu de la regla.**
Se reformuló: la evidencia puede estar en cualquier archivo, lo que no puede faltar es el
**vínculo con una salida real**. Con eso el caso vuelve a 89 y la exigencia sigue midiendo lo que
tenía que medir — si el sistema sirvió, no dónde se escribió que sirvió.

> Es la tercera vez que una regla nuestra falla al primer contacto con un caso concreto (D-4, D-13,
> y ahora ésta). Escribir la regla y verificarla contra los casos **en el mismo movimiento** debería
> ser el procedimiento, no una revisión posterior.

---

## Lo que este ensayo NO probó

- **Un lote de verdad.** Seis trabajos, no cincuenta. La deriva de la vara, si existe, aparece con
  volumen — y con cincuenta trabajos aparece además el problema de discriminación anotado como
  **E-4** en la autocrítica.
- **La entrada de Moodle.** La tanda se armó a mano; nunca procesamos el árbol de "Descargar todas
  las entregas" ni produjimos la hoja de calificaciones. El formato está verificado
  (`agente/lote.md` §1), el recorrido completo no.
- **Repositorios ajenos de verdad.** Cuatro de los seis son casos nuestros. El único ajeno terminó
  —correctamente— sin nota, así que este lote no midió la vara contra ningún trabajo final real.
