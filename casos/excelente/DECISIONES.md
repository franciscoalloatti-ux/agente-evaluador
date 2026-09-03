# Decisiones — cómo llegué acá

## Iteración 1 — 27/8 · "armame una ficha de cada licitación"

**Qué probé.** El prompt más directo posible: le pegué el CSV y le pedí "leé estas licitaciones y
armame una ficha corta de cada una que sea para un estudio de arquitectura".

**Qué falló.** Dos cosas. Primero, me devolvió las 41 fichas, incluidas las de Vialidad y las de
provisión de bienes: entendió "para un estudio de arquitectura" como un pedido de tono, no como un
filtro. Segundo, cada ficha tenía una estructura distinta; algunas traían presupuesto, otras no,
otras traían un "análisis de conveniencia" de tres párrafos que yo no había pedido.

**Qué cambié.** Separé el contrato en system y user prompt. En el system puse el rubro **como lista
explícita de qué sí y qué no** (incluyendo el "no hacemos vialidad, ni obra hidráulica de gran
escala, ni provisión de bienes") y fijé los 9 campos de la ficha.

---

## Iteración 2 — 3/9 · el presupuesto inventado

**Qué probé.** La corrida del 3/9 sobre 55 avisos, ya con el contrato separado.

**Qué falló.** El aviso `EX-2026-0044177` (Villa Allende) venía con la columna `presupuesto`
vacía. El agente devolvió:

```
"presupuesto_oficial": 24000000,
"motivo_senal": "Monto estimado en línea con obras similares del municipio"
```

No había ningún monto en el aviso. Lo estimó. Y lo peor es que lo dijo con una frase que suena
razonable: si no hubiera abierto el CSV, me lo creía. Ese número, en la reunión de comercial, es
una decisión de presentarse a algo que no sabemos cuánto vale.

**Qué cambié.** Agregué la restricción 1 del system prompt, textual:

> *"Si un campo no está en el aviso, devolvé `null`. Nunca lo estimes ni lo completes con el
> promedio de los otros avisos."*

Volví a correr el mismo CSV y salió `null` (está en `corridas/2026-09-03_radar.md`). El antes y el
después son el mismo archivo de entrada, así que la comparación es limpia.

---

## Iteración 3 — 4/9 · el intento de arreglar el `null`, y por qué lo abandoné

**Qué probé.** El `null` era correcto pero me obligaba a abrir el aviso a mano. Como varios avisos
publican el presupuesto dentro del texto de `descripcion`, le pedí que lo buscara ahí cuando la
columna estuviera vacía.

**Qué falló.** Empezó a traer números que no eran plata:

```
"presupuesto_oficial": 120,
"motivo_senal": "Presupuesto extraído de la descripción del aviso"
```

Ese 120 era el **plazo de obra en días**. En otro caso trajo 2.400, que eran los metros de
canalización. El agente encontraba un número y lo trataba como monto.

**Qué cambié — y qué achiqué.** Abandoné la idea y la convertí en la restricción 3 del system
prompt: *"No busques el presupuesto dentro del campo `descripcion`."* Preferí que me falte el dato
antes que tener un dato falso que parece verdadero. Es la decisión de alcance más importante del
trabajo: renuncié a automatizar el 100 % para no romper la confianza en el 90 %.

---

## Lo que quedó roto

**Sigue sin resolverse:** los avisos con el presupuesto sólo en el texto siguen saliendo `null` y
los abro a mano. En la corrida del 5/9 fueron 1 de 4 fichas. Sé cuál sería el camino
—leer el pliego adjunto en vez del CSV, que es un PDF— pero no llegué a probarlo en estas dos
semanas y no quería entregar una integración a medias.

**Lo que decidí no medir:** no tengo una medición sistemática de cuántas veces la `senal` acierta.
Miré 31 fichas a ojo y 7 quedaron en `revisar`, pero no llevé registro de en cuántas yo hubiera
decidido distinto. Es lo primero que haría si esto siguiera.

---

## Registro de cambios del contrato

| Fecha | Archivo | Qué cambió | Motivo |
|-------|---------|-----------|--------|
| 27/8 | — | Prompt único, en el chat | Punto de partida |
| 28/8 | `prompts/system_prompt.md`, `prompts/user_prompt.md` | Contrato separado, rubro explícito, 9 campos fijos | Iteración 1 |
| 3/9 | `system_prompt.md` restricción 1 | Regla del `null` | Iteración 2 |
| 3/9 | `system_prompt.md` restricción 2 | Mapeo de columnas por nombre | Salió del mismo análisis: si cambia el CSV, cruza los campos |
| 4/9 | `system_prompt.md` restricción 3 | Prohibición de buscar monto en `descripcion` | Iteración 3 |
| 5/9 | `user_prompt.md` | Línea de conteo ("N avisos leídos, M del rubro") | Para saber si leyó el archivo entero sin abrirlo |
