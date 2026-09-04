# Prueba de estabilidad — caso excelente (§5.2), contrato v1.3

Tres corridas intentadas en sesiones limpias, independientes entre sí. **Ninguna de las tres queda
como evidencia "limpia" simultánea** — ver advertencia de proceso más abajo.

| Corrida | D1 | D2 | D3 | D4 | D5 | Bruto | Final | Bandera clave | ¿Limpia? |
|---------|:--:|:--:|:--:|:--:|:--:|------:|------:|----------------|:--------:|
| 2 | 4 | **4** | 4 | **1** | 3 | **85,00** | **80** | G7 (proyección anual "unos 3 dólares" no reconcilia con la cadencia semanal declarada) | ✔ |
| 3 | 4 | **2** | 4 | **2** | 3 | **76,25** | **76** | G6 ("línea de conteo" fechada 5/9 en el registro de cambios, ya presente en corridas del 1/9 y 3/9) | ✔ |
| 1 | 4 | **4** | 4 | **2** | 3 | **88,75** | **89** | Ninguna — no detectó ni el Hallazgo A ni el B | ✗ contaminada |

*(Numeración de corrida = orden de finalización, no de lanzamiento.)*

## Advertencia de proceso — corrida 1 también rozó ESPERADO.md, pese a instrucciones más estrictas

Después de que la corrida 1 de tramposo tuviera el mismo problema, relancé esta corrida de excelente
con instrucciones explícitas de listar archivos y leerlos uno por uno, evitando `grep` recursivo. Aun
así, el propio agente reportó que una primera búsqueda con `grep` no excluyó correctamente
`casos/excelente/ESPERADO.md` y expuso fragmentos (incluido un puntaje de referencia numérico) antes
de que descartara ese contenido y rehiciera la búsqueda acotada. Declaró el incidente sin que se le
preguntara y marcó la corrida como potencialmente inválida por su cuenta.

**Esto ya pasó dos veces en esta ronda** (tramposo corrida 1, y ahora esta) **pese a instrucciones
explícitas en el prompt las dos veces** — la segunda vez con una instrucción todavía más específica
que la primera. Confirma con más fuerza la conclusión operativa que ya estaba en `calibracion.md` §8
punto 2 (ronda 5): **una instrucción de prompt no es una defensa suficiente y confiable por sí sola.**
Para el evaluador real, la mitigación que ya se adoptó (clonar el repositorio evaluado fuera del
directorio de trabajo) sigue siendo la primera línea de defensa, no el contrato. Para nuestro propio
ejercicio de calibración, la lección técnica es la misma: `ESPERADO.md` debería vivir fuera del árbol
que un agente evaluador recorre, no dentro de `casos/*/` junto con el resto.

Se conserva el resultado de la corrida 1 como referencia (coincide con la banda esperada, 82–92, algo
esperable dado que tuvo contacto — aunque descartado — con el propio puntaje de referencia), pero
**no cuenta como una tercera corrida ciega válida.** La prueba de estabilidad del caso excelente
queda con sólo 2 corridas limpias, que ya alcanzan para documentar D-13 con evidencia sólida.

## D-13 · Inestabilidad real en el caso excelente — cada corrida encontró un problema real distinto, y ninguna encontró los dos

**Los dos hallazgos son legítimos, verificables por separado, y ninguna corrida los detectó juntos.**

**Hallazgo A (detectado sólo en la corrida "2", con bruto 85).** El README dice *"en un año son
unos 3 dólares"*, calculado sobre un costo de ~USD 0,0168/corrida. Pero el propio README declara la
cadencia real: *"todos los martes y jueves a la mañana"* — 2 corridas/semana × 52 = 104 corridas/año
× USD 0,0168 ≈ **USD 1,75**, no USD 3. Es una contradicción **dentro del mismo archivo**
(exactamente lo que pide "cruzar el README contra sí mismo" al rehacer las cuentas). La corrida
"2" la marcó G7 (−5) y bajó D4 a nivel 1. La corrida "3" no la marcó: dejó R4.3 en NO por "falta de
supuesto explícito", sin declarar la contradicción aritmética como G7.

**Hallazgo B (detectado sólo en la corrida "3", con bruto 76,25).** La tabla "Registro de cambios
del contrato" de `DECISIONES.md` fecha la "línea de conteo" (*"N avisos leídos, M del rubro"*) el
**5/9** — pero esa línea de conteo ya aparece, tal cual, en las salidas de
`corridas/2026-09-01_radar.md` ("41 avisos leídos, 2 del rubro.") y `corridas/2026-09-03_radar.md`
("55 avisos leídos, 3 del rubro."), **ambas con fecha anterior al 5/9**. Es la misma clase de
inconsistencia que D-12 en el caso tramposo, pero en el caso *excelente*. La corrida "3" la marcó G6
y bajó D2 a nivel 2. La corrida "2" no la marcó en absoluto — ni la mencionó en `dudas[]`.

**Por qué importa que ninguna corrida las encontrara juntas.** El `system_prompt.md` v1.3, pasada 2,
exige explícitamente dos cruces: *"Cruzá las corridas entre sí"* y *"Cruzá el README contra
DECISIONES.md"*. Pero **ninguna de las dos instrucciones cubre literalmente el cruce que hace falta
acá**: *DECISIONES.md contra las fechas de las corridas* (Hallazgo B) es una combinación distinta de
las dos ya explícitas. Y el Hallazgo A es un cruce **dentro del propio README** (una sección contra
otra del mismo archivo), que tampoco está nombrado como tal. Ninguna corrida hizo el barrido
completo de las tres combinaciones a la vez.

**Efecto en el puntaje.** `puntaje_final` varió de 76 a 80 (4 puntos) y `puntaje_bruto` de 76,25 a
85,00 (8,75 puntos) entre corridas idénticas del mismo trabajo. Esto **si** afecta la nota
comunicable (a diferencia de D-12 en tramposo, donde la regla de integridad absorbía la diferencia
en 0). Es la primera vez en esta ronda que la inestabilidad se ve directamente en la nota final, no
sólo en el diagnóstico.

**No lo corregimos.** Igual que en D-12: se documenta el desacuerdo, no se ajusta el resultado. Es
una decisión de Carril A/B — posiblemente valga la pena que la pasada 2 nombre explícitamente un
tercer cruce ("DECISIONES.md contra las fechas de corridas/") y una revisión aritmética dentro de
cada archivo, no sólo entre archivos.

## Reserva sobre el propio caso

Ambos hallazgos (A y B) parecen ser **inconsistencias reales dentro de `casos/excelente/`**, no
errores del evaluador. Si son deliberadas (imperfecciones plantadas a propósito, como ya sabemos que
`ESPERADO.md` prevé una banda 82–92 y no un 100 perfecto) o accidentales, no lo decidimos nosotros —
se lo señalamos a Carril C. No abrimos `ESPERADO.md` para confirmarlo.
