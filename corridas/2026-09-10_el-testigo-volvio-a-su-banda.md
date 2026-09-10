# El testigo volvió a su banda — y de paso dio vuelta lo que decíamos del determinismo

**Fecha:** 2026-09-10 · **Contrato:** v1.12 → **v1.13** · **Modelo:** Claude Sonnet 5 vía API,
**sin `temperature`** (la API la rechaza)
**Cómo se corrió:** `casos/excelente/` completo, con `ESPERADO.md` **excluido del paquete**, tres
veces en sesiones limpias

---

## Lo que había que contestar

Esa misma mañana el testigo había caído de 89 a **65** y tenía razón al hacerlo: encontró una
contradicción entre el `system_prompt.md` y el `user_prompt.md` del caso, que habíamos introducido
nosotros el 31/8 (`2026-09-10_el-testigo-tenia-un-defecto.md`). Corregimos el caso —declarando la
línea de conteo en vez de prohibirla— y quedó pendiente lo único que importaba:

> **Volver a correrlo y fijar la banda con el número que dé.** Hasta entonces el caso no sirve como
> testigo: un testigo que no da su propio valor no puede detectar deriva.

Con una condición que no se negocia: **el número sale de la corrida.** Si daba 71, la banda pasaba a
ser 71. Corregir un caso para llegar a un número es exactamente lo que le penalizamos a los demás.

---

## El resultado

| Corrida | Final | Bruto | D1 | D2 | D3 | D4 | D5 | Banderas |
|---|---:|---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | **89** | 88,75 | 4 | 4 | 4 | 2 | 3 | ninguna |
| 2 | **89** | 88,75 | 4 | 4 | 4 | 2 | 3 | ninguna |
| 3 | **89** | 88,75 | 4 | 4 | 4 | 2 | 3 | ninguna |

**Volvió exacto a 89**, dentro de la banda 82–92 que tenía antes de que rompiéramos el caso. Y los
dos huecos que el `ESPERADO.md` planta a propósito siguen encontrados: **D4 en 2** (no hay proyección
económica) y **D5 en 3** (sólo dos modos de falla). El caso vuelve a ser un testigo válido.

**Además, cero hallazgos de auditoría.** En las tres corridas cada nivel coincide **exactamente** con
su cuenta de requisitos en `SI` — ni un `A4`, ni un `A4 bis`. Es la primera verificación del chequeo
que habíamos agregado horas antes.

---

## Lo que no esperábamos, y es más importante que la banda

Las tres corridas son **idénticas**: mismo final, mismo bruto, **los cinco niveles** y las mismas
banderas (ninguna). **Sin poder fijar la temperatura.**

Ese mismo día habíamos escrito que no pasábamos la prueba de estabilidad, con cinco corridas de
16 · 18 · 25 · 25 · 29 sobre un repositorio real. Las dos cosas son ciertas y juntas dicen algo que
por separado no decían:

| Trabajo | Corridas | Resultado |
|---|---|---|
| `pool-de-los-miercoles` — real, con ausencias y zonas grises | 5 | 16 · 18 · 25 · 25 · 29 |
| `casos/excelente/` — completo, con evidencia citable | 3 | **89 · 89 · 89** |

> **La dispersión no la pone el modelo: la pone el trabajo.**

Cuando la evidencia está y se puede citar, el contrato converge aunque el muestreo esté suelto —
porque el nivel se **deriva de contar requisitos**, no de opinar sobre ellos. Cuando el trabajo es
ambiguo, cada corrida resuelve la ambigüedad a su manera, y **el desacuerdo del modelo consigo mismo
mide cuánta interpretación dejamos abierta**.

Encaja con dónde se movía la variación: en **D1 y D5**, las dos dimensiones donde nuestros propios
requisitos admiten más de una lectura, y las mismas donde difirieron los dos humanos que puntuaron a
ciegas. D2, D3 y D4 daban idénticos.

---

## Qué se cambió en el contrato

`rubrica.md` **§3, condición 1**, ya no dice *"no pasamos la prueba de estabilidad"*. Dice lo que se
midió: **el determinismo es condicional a que el requisito esté anclado**, no a que el proveedor deje
fijar una perilla. Anclar D1 y D5 sigue siendo la respuesta de fondo, y ahora se sabe por qué
funciona.

---

## Lo que este hallazgo NO permite decir

Que el evaluador es determinista. **Tres corridas sobre un caso son evidencia, no demostración**, y
es el caso que escribimos nosotros — el mismo sesgo de local que nos costó el defecto de la mañana.
Lo que corresponde: repetirlo sobre un trabajo ajeno bien documentado. Si ahí también converge, la
afirmación se sostiene; si no, la que se corrige es la §3.

Queda anotado como lo que es: **una hipótesis con tres corridas a favor**, no un resultado cerrado.
