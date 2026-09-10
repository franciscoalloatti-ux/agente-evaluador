# El nivel que salió de la prosa, no de la cuenta

**Fecha:** 2026-09-10 · **Contrato:** v1.11 → **v1.12** · **Origen:** revisión de los informes ya
guardados de la prueba de estabilidad

---

## Cómo apareció

La prueba de estabilidad del mismo día dejó una conclusión cómoda: *"D2, D3 y D4 dieron idénticos
las cinco veces; toda la variación está en D1 y D5"*. Antes de firmarla fuimos a mirar los informes
crudos, requisito por requisito, en vez de quedarnos con los niveles.

**D3 fue idéntico las cinco veces, pero idénticamente mal.**

| Informe | Final | D3 nivel | Requisitos D3 en `SI` |
|---|---:|:---:|:---:|
| corrida 4 | 29 | **1** | **0** |
| corrida 5 | 18 | **1** | **0** |
| corrida 2 | 25 | 1 | 1 |

Dos de los tres informes guardados declaran **nivel 1 con cero requisitos cumplidos**. Según la
§0.2, cero `SI` es nivel 0. La compuerta puede bajar, nunca subir.

---

## De dónde salió ese punto

De la justificación. Textual, del informe de la corrida 4:

> *"R3.2 se corrige: al releer el README letra por letra, los cinco encabezados coinciden
> exactamente con los exigidos por la rúbrica…"*

Y en la corrida 5, casi con las mismas palabras:

> *"Corrigiendo R3.2: el README sí trae los cinco encabezados exactos con contenido (E1, E10, E12),
> por lo que R3.2 = SI."*

**El modelo cambió de opinión escribiendo, subió el nivel para reflejarlo, y no volvió a tocar el
array.** El campo `cumple` de R3.2 quedó en `false` en los dos informes. El nivel salió de la prosa.

Es exactamente lo que la §0.2 existe para impedir —*el nivel no se elige, se deriva*— y pasó adentro
de nuestro propio contrato, dos veces, sobre el mismo repositorio.

---

## Por qué el chequeo A4 no lo frenó

**Sí lo detecta.** `A4` compara nivel contra la cuenta de `SI` y estos dos informes lo violan. Lo que
falló no es el chequeo: es que estas corridas se hicieron con el script de estabilidad, que llama al
relay directo y **guarda el JSON sin pasarlo por `validar()`**. La red estaba puesta y la pelota
pasó por al lado.

> Lo anotamos porque es el mismo error que penalizamos con **A9**: *un cruce sin reportar es
> indistinguible de uno no hecho*. Un chequeo que existe pero no se corre vale lo mismo que ninguno.

---

## El agujero que sí era del contrato

Buscando el caso al revés apareció otro, y ése no lo cubría nada: **el nivel por debajo de la
cuenta.**

| Informe | Dim | Nivel | `SI` | ¿Nombra la compuerta? |
|---|---|:---:|:---:|---|
| corrida 2 | D5 | 2 | 3 | **Sí** — *"la compuerta dura de R5.4 = NO fija D5 ≤ 2"* |
| otro informe | D2 | 1 | 2 | **No** |

El primero está impecable: baja el nivel y **cita la regla que lo baja**. El segundo baja el nivel y
no dice por qué. Los dos pasaban la validación igual, porque `A4` sólo miraba hacia arriba.

Un nivel más bajo que la cuenta, sin compuerta nombrada, **es un descuento a ojo** — y vale
exactamente lo mismo que un aumento a ojo. La asimetría era nuestra: perseguíamos la generosidad y
dejábamos pasar la severidad, cuando las dos rompen la misma regla.

---

## Qué se cambió

**En el contrato** (`agente/system_prompt.md`, pasada 3):

- **6ter** — el array de requisitos es la única fuente del nivel. Si cambiás de opinión al escribir
  la justificación, volvé y cambiá `cumple`. La justificación no corrige al array.
- **6quater** — si una compuerta bajó el nivel por debajo de la cuenta, **nombrala con su texto**.
- La fila `A4` de la tabla de auditoría ahora cubre las dos direcciones.

**En la rúbrica** (§0.2): la regla, con el caso que la originó.

**En la consola** (`validar()`): el mensaje de `A4` ahora dice *qué* hay que corregir —el campo
`cumple`, no el nivel— y se agrega **`A4 bis`**, que marca el nivel por debajo de la cuenta cuando la
justificación no nombra ninguna compuerta.

**En el banco de pruebas:** dos casos nuevos. Uno que tiene que saltar (nivel 2 con 4 requisitos en
`SI`, sin explicación) y **uno que no tiene que saltar** (el mismo nivel, con la compuerta nombrada).
El segundo importa tanto como el primero: un chequeo que también protesta cuando está todo bien
enseña a ignorarlo. **36 pruebas, 36 en verde.**

---

## Lo que este hallazgo dice, y lo que no

**No dice** que la prueba de estabilidad estuviera mal: los cinco números —16, 18, 25, 25, 29— son
los que dio el evaluador y siguen siendo el dato.

**Sí dice** que la lectura era optimista. *"D3 fue estable"* era falso en el único sentido que
importa: fue **consistentemente incorrecta**, que es peor que inestable. Una dimensión que se
equivoca siempre igual no se nota mirando la dispersión — hay que abrir el array.

Y deja una regla de método: **la estabilidad se mide sobre informes validados.** Un informe que no
pasó por los nueve chequeos no es un dato de estabilidad, es un dato de otra cosa.
