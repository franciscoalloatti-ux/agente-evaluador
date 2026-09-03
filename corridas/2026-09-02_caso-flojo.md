# Corrida — caso `flojo`

**Fecha:** 2026-09-02 · **Contrato:** v1.1, **re-corrido con v1.2 sin cambios** · **Modelo:** Claude Opus 5, temperatura 0
**Camino:** A (lectura local) · **Formato:** variante corta
**Entrada:** `casos/flojo/` · **Operador:** *(completar)*

---

## Puntaje

| Dimensión | Peso | Nivel | Puntos |
|-----------|-----:|:-----:|-------:|
| D1 · Sistema completo y funcionando | 30 | 1/4 | 7,50 |
| D2 · Proceso documentado | 25 | 1/4 | 6,25 |
| D3 · Formato y reproducibilidad | 15 | 1/4 | 3,75 |
| D4 · Análisis económico | 15 | 0/4 | 0,00 |
| D5 · Gobierno y riesgo | 15 | 0/4 | 0,00 |
| **Bruto** | | | **17,50** |
| Penalizaciones | | | **0,00** |
| **Final** | | | **18 / 100 — nota 1,8** |

**Estado:** `evaluado` · `revision_humana_requerida: false`

## Una línea por dimensión

- **D1 · 1/4 · 7,50** — `[E1][E2]` cinco de las seis piezas están (rol, contexto, tarea,
  restricciones, formato); falta **ejemplos**, y la rúbrica pide que falten dos o más para dar NO:
  **R1.1 = SI**. R1.2 = NO: no hay herramienta, el usuario tipea el puesto y pega la respuesta.
  R1.3 = NO: el formato está especificado pero hay **dos** corridas, no tres. R1.4 = NO: sin
  nivel de delegación, sin control humano declarado, sin firma. Compuerta R1.2 → D1 ≤ 2.
- **D2 · 1/4 · 6,25** — R2.2 = SI: hay un error textual pegado tal cual `[E5]`
  `Job Title: Sales Representative / Reports to: Regional Sales Manager`, la salida en inglés que
  motivó el cambio. R2.1, R2.3 y R2.4 = NO. Compuerta: no existe `DECISIONES.md` → D2 ≤ 1.
- **D3 · 1/4 · 3,75** — R3.1 NO (falta `DECISIONES.md`); R3.2 NO (el README tiene cuatro de las
  cinco secciones: falta **"Qué falta o qué falló"**); R3.3 NO (dos corridas, ninguna fechada);
  R3.4 SI `[E6][E7]` (el puesto pedido aparece en la salida). Compuerta: menos de 3 corridas → D3 ≤ 1.
- **D4 · 0/4 · 0,00** — la única mención es `[E8]` *"El costo no lo calculé pero debe ser muy bajo"*.
- **D5 · 0/4 · 0,00** — **ver la duda registrada abajo.**

## Banderas

**Ninguna.** En particular, **no** se marcó G1 sobre `[E8]` ni sobre *"para puestos técnicos no lo
probé"*: el trabajo no afirma haber hecho lo que no hizo, admite que no lo hizo. Eso ya está
castigado por vía del puntaje; marcarlo como bandera sería castigarlo dos veces.

Tampoco G4: el README es corto, y la brevedad no es relleno.

## Sugerencia de mejora

```
D1: 30 x 3/4 = 22,50   <- mayor
D2: 25 x 3/4 = 18,75
D4: 15 x 4/4 = 15,00
D3: 15 x 3/4 = 11,25
D5: 15 x 4/4 = 15,00
```

**D1 — hasta 22,5 puntos.** Darle al agente una fuente que leer en vez de un nombre tipeado: por
ejemplo la planilla de puestos vigentes de RRHH, de la que salgan el área, el reporte jerárquico y
el convenio. Guardar una tercera corrida, con fecha. Es lo que levanta R1.2 y con él la compuerta
que hoy topea la dimensión.

## Reservas del evaluador

> **Duda registrada — R5.3.** El README dice que las descripciones *"las puedo pegar directo en la
> plantilla de RRHH"*. Eso describe el destino de la salida, no un control previo. El requisito
> exige *qué revisa la persona antes de confiar, en concreto*, y eso no está escrito en ninguna
> parte. Aplicando `rubrica.md` §0.4 —duda hacia el nivel menor— se resolvió **R5.3 = NO**, con lo
> que D5 queda en nivel 0.
>
> Con R5.3 = SI el total sería 21 en lugar de 18. Ambos caen dentro de la banda esperada; la
> diferencia se deja asentada acá para que sea discutible.

**Firma:** agente-evaluador v1.1 · Claude Opus 5 · temperatura 0
**Responsable humano:** *(completar)*

---

## Comparación contra `casos/flojo/ESPERADO.md`

| | Esperado | Obtenido | ¿Coincide? |
|---|---|---|---|
| Puntaje final | 21, o 17 si R5.3 = NO (banda 15–30) | 18 | Sí — la banda y la resolución severa prevista |
| Niveles D1–D5 | 1 · 1 · 1 · 0 · 1 ó 0 | 1 · 1 · 1 · 0 · 0 | Sí |
| Duda de R5.3 registrada | obligatorio | registrada | Sí |
| Banderas | ninguna | ninguna | Sí |

> **Nota.** El `ESPERADO.md` anticipaba 17 para la rama severa y el agente devolvió 18. La
> diferencia es de redondeo: `1/4 × 30 + 1/4 × 25 + 1/4 × 15 = 17,50`, que con redondeo medio hacia
> arriba da **18**, no 17. El `ESPERADO.md` tenía mal la cuenta, no el agente.
> Corregido en `calibracion.md`, discrepancia **D-5**.
