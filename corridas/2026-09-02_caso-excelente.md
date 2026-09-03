# Corrida — caso `excelente`

**Fecha:** 2026-09-02 · **Contrato:** v1.1, **re-corrido con v1.2 sin cambios** · **Modelo:** Claude Opus 5, temperatura 0
**Camino:** A (lectura local) · **Formato:** variante corta de `agente/plantilla_informe.md`
**Entrada:** `casos/excelente/` · **Operador:** *(completar)*

El JSON completo se emitió igual; acá se transcribe la variante corta, que es la que se usa en la
prueba de fuego.

---

## Puntaje

| Dimensión | Peso | Nivel | Puntos |
|-----------|-----:|:-----:|-------:|
| D1 · Sistema completo y funcionando | 30 | 4/4 | 30,00 |
| D2 · Proceso documentado | 25 | 4/4 | 25,00 |
| D3 · Formato y reproducibilidad | 15 | 4/4 | 15,00 |
| D4 · Análisis económico | 15 | 2/4 | 7,50 |
| D5 · Gobierno y riesgo | 15 | 3/4 | 11,25 |
| **Bruto** | | | **88,75** |
| Penalizaciones | | | **0,00** |
| **Final** | | | **89 / 100 — nota 8,9** |

**Estado:** `evaluado` · `revision_humana_requerida: false`

## Una línea por dimensión

- **D1 · 4/4 · 30,00** — `[E3]` las seis piezas rotuladas en `prompts/system_prompt.md`;
  `[E7][E11]` el expediente `EX-2026-0044178` aparece en la corrida y no está en el prompt: la
  herramienta es real y su dato es irreproducible sin ella; `[E9]` mismos 9 campos en las tres
  corridas; `[E14]` "Nivel de delegación: L2" con qué revisa y quién firma. Nivel 4 pleno.
- **D2 · 4/4 · 25,00** — `[E16]` tres iteraciones fechadas con la tríada; `[E17]` error textual
  pegado tal cual: `"presupuesto_oficial": 24000000` sobre un aviso que no publicaba monto;
  `[E18]` el `120` que era el plazo de obra tomado como precio; `[E19]` abandona la extracción
  desde `descripcion` con su razón. La sección "Lo que quedó roto" `[E20]` cumple la exigencia
  extra de nivel 4: una falla no resuelta, contada con precisión.
- **D3 · 4/4 · 15,00** — `[E1]` los cuatro elementos en la raíz; `[E2]` los cinco encabezados
  exactos; `[E7][E10][E12]` tres corridas con entrada, salida y fecha, con entradas distintas.
- **D4 · 2/4 · 7,50** — `[E21]` 11.250 y 1.100 tokens discriminados; `[E22]` precio con fecha de
  consulta y la cuenta escrita, **rehecha por el evaluador: 0,01125 + 0,0055 = 0,0168; cierra**.
  Pero `[E23]` "en un año son unos 3 dólares" no declara cuántas corridas por semana (R4.3 = NO) y
  `[E24]` "usé el modelo liviano porque alcanza y sobra" no compara con ningún otro (R4.4 = NO).
- **D5 · 3/4 · 11,25** — `[E25]` permisos por sistema y qué **no** toca; `[E27]` control humano
  concreto (verifica fecha de apertura y expediente contra el aviso original); `[E28]` firma con
  nombre y rol. Falta R5.2: hay **dos** modos de falla `[E26]`, la rúbrica exige tres.

## Banderas

**Ninguna.**

Punto de control explícito: la sección "Qué falta o qué falló" describe cosas que no funcionan
`[E20]`. Eso es honestidad documentada y suma en D2/R2.3. **No** se marcó G1: el trabajo no afirma
haber resuelto lo que no resolvió.

## Sugerencia de mejora

**D4 — hasta 7,5 puntos.** Agregar dos líneas al bloque "Análisis económico" del README: el
supuesto de volumen de la proyección (corridas por semana × semanas) y el resultado de correr una
misma corrida con un segundo modelo, mostrando en qué se diferenciaron las salidas. Con eso R4.3 y
R4.4 pasan a SI y la dimensión sube de nivel 2 a nivel 4.

## Reservas

Ninguna. Sin acceso a commits, R2.4 se verificó contra las fechas de `corridas/`, que se
corresponden con las iteraciones 2 y 3 de `DECISIONES.md`.

**Firma:** agente-evaluador v1.1 · Claude Opus 5 · temperatura 0
**Responsable humano:** *(completar)*

---

## Comparación contra `casos/excelente/ESPERADO.md`

| | Esperado | Obtenido | ¿Coincide? |
|---|---|---|---|
| Puntaje final | 89 (banda 82–92) | 89 | Sí |
| Niveles D1–D5 | 4 · 4 · 4 · 2 · 3 | 4 · 4 · 4 · 2 · 3 | Sí |
| Banderas | ninguna | ninguna | Sí |
| Sugerencia | D4, 7,5 pts | D4, 7,5 pts | Sí |
