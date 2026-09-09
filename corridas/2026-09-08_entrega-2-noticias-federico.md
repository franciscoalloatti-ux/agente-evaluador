# Corrida — repositorio real (§5.3): `federicobofer/entrega-2-agente-noticias-economicas`

> **Nota de procedencia.** Es la Entrega 2 real de Federico Böfer para esta misma cursada
> (el README lo declara en la línea 3). Real y fuera de muestra, nunca vista antes por el agente;
> no "ajena" en sentido estricto — misma reserva que las tres entregas de Verónica en §5.3.

**Fecha de corrida:** 2026-09-08 · **Contrato:** v1.10 · **Camino A** (clon aislado en
`~/re/e2`, 2 commits reales del 2026-08-27).

**Resultado:** D1=1/4 · D2=1/4 · D3=3/4 · D4=0/4 · D5=0/4 · `puntaje_bruto` = 25,00 ·
`puntaje_final` = 25/100 (nota 2,5) · `estado` = `evaluado_con_reservas` ·
`revision_humana_requerida` = true. **Sin banderas.**

## Inventario

- `config_agentes_hallada`: `[]` (sin `AGENTS.md` / `CLAUDE.md` / `.cursorrules`).
- `raiz_efectiva`: `.` — `formato_entrada`: `repositorio_git`.
- Estructura obligatoria: `README.md` presente · `prompts/` **ausente** (el contrato está en
  `system_prompt.md` + `user_prompt.md` en la raíz) · `corridas/` **ausente** (`salida_1/2/3.md`
  en la raíz) · `DECISIONES.md` **ausente** (el proceso vive en la sección "Las dos iteraciones"
  del README y en `iteraciones/`).
- Barrido G8 y de caracteres invisibles sobre los 14 archivos (incluidos los 3 `.html` de
  `plataforma/`): limpio. Las `.html` piden la API key al usuario y la guardan en `localStorage`;
  no hay credencial versionada.

## Puntuación

| Dim | Requisitos | Compuerta | Nivel · pts |
|-----|-----------|-----------|-------------|
| **D1** | R1.1 **SI** (6 piezas rotuladas en `system_prompt.md` v3) · R1.2 **NO** (el contrato dice *"Trabajás solo con el texto que te pasa el usuario. No tenés acceso a internet"*; las 3 salidas son texto pegado) · R1.3 **NO** (las 3 corridas tienen esquemas distintos a propósito — v1/v2/v3) · R1.4 **NO** (sin L0–L4, sin firma de responsable) | R1.2=NO → D1≤2 · sin `prompts/` → **D1≤1** · objetivo declarado, su compuerta no actúa | **1 · 7,50** |
| **D2** | R2.1 **NO** (documenta **2** iteraciones con la tríada completa; la rúbrica exige 3) · R2.2 **SI** (`salida_1.md`, N1 con `impacto: alto` justificado por tema) · R2.3 **SI** ("Qué aprendí": *"mi restricción decía 'según su relevancia'… La pieza estaba floja, no el modelo"*) · R2.4 **NO** (2 commits, ambos del 27/8; ninguno refleja una iteración) | no existe `DECISIONES.md` → **D2≤1** | **1 · 6,25** |
| **D3** | R3.1 **NO** (falta `prompts/`, `corridas/`, `DECISIONES.md`) · R3.2 **SI** (las 5 secciones exactas) · R3.3 **SI** (`salida_1/2/3.md` con salida, entrada referida y fecha de corrida) · R3.4 **SI** (`user_prompt.md` + `iteraciones/system_prompt_v1.md` reproducen `salida_1`) | ninguna (hay 3 corridas, no idénticas) | **3 · 11,25** |
| **D4** | R4.1–R4.4 **NO** (el repo no calcula tokens, costo ni proyección; R4.4 menciona la elección de modelo pero dice que la comparación falta) | faltan tokens/precio → D4≤2 | **0 · 0,00** |
| **D5** | R5.1 **NO** (sin inventario de permisos) · R5.2 **NO**/duda (lista limitaciones; alcanzo 2 con tríada, no 3) · R5.3 **NO**/duda (*"lo tiene que ver el humano"* + `consola-agente.html`, pero *"no es parte del contrato"*) · R5.4 **NO** (*"Autor: Federico Bofer"* es autoría, no firma de responsable con rol) | R5.4=NO → D5≤2 | **0 · 0,00** |

## Cruces (batería de 7)

C1–C7 ejecutados, **ningún hallazgo**. C7 confirma que `salida_3` es del `system_prompt.md` v3
(12 campos, orden por `impacto_magnitud`, conteos que cierran: alto 2 + medio 3 = `n_noticias` 5).
La aritmética embebida en las noticias cierra (N3: 103.740/88.846 = +16,8% ≈ el "~17%" citado;
N4: 28.000/11.320 = 2,47 ≈ "2,5 veces").

## Qué se rompió

1. **El patrón de las entregas de Verónica, otra vez, y más nítido.** Contrato de 6 piezas
   genuinamente bueno, 2 iteraciones bien contadas con su error textual, README estándar completo,
   3 corridas reales y reconstruibles con links verificados. Y el puntaje es 25, aplastado por
   **dos compuertas de nombre de archivo**: sin `prompts/` (D1≤1) y sin `DECISIONES.md` (D2≤1).
   D2 por conteo de requisitos daría nivel 2 y la compuerta lo deja en 1.

2. **Choque de consigna, no de calidad.** El repo se autodeclara "Entrega 2" y está construido
   para *esa* consigna: mostrar la evolución v1→v2→v3 (por eso las 3 corridas tienen esquemas
   distintos: es el punto) y documentar **dos** iteraciones (la Entrega 2 pedía dos; el TF pide
   tres). Evaluado como trabajo final, cada una de esas decisiones correctas para la Entrega 2 se
   lee como un requisito incumplido. Por eso `revision_humana_requerida: true`: un humano decide si
   corresponde puntuar un repo de Entrega 2 con la vara del TF.

3. **Hueco de la rúbrica — R3.3 y la ambigüedad forma/fondo.** R3.3 dice *"Tres corridas guardadas
   **en `corridas/`**"*. Lo evalué por contenido (§0.4: la ubicación se cobra una sola vez, en
   R3.1) y di R3.3 = SI. Un evaluador que lea R3.3 como requisito de ubicación baja D3 de 3 a 1 y
   el final de 25 a ~19. **Es la misma ambigüedad forma/fondo que el grupo ya cerró en §0.4 pero
   que sigue viva en la redacción de R3.3.** → carril A.

4. **Hueco de la rúbrica — D3 = 3 sin entradas distintas.** Las 3 corridas son del mismo día
   (27/8) sobre la misma entrada. El nivel 3 no exige entradas distintas (sólo el extra de nivel 4
   lo hace). Un ejercicio de iteración bien ordenado —el que pedía la Entrega 2— saca D3 = 3 en la
   rúbrica del TF. Ninguno de los 3 casos construidos podía mostrar esto porque los 3 tienen
   corridas con entradas distintas. → carril A.

5. **G6 no verificable.** 2 commits del mismo día con un relato de 2 iteraciones hechas "el del
   taller". Plausible en una sesión, no fabricado. Registrado en `dudas[]` sin tocar el puntaje.

## Nota al margen (interna)

Nota extrema baja (25 < 40). Releerla contra el caso testigo (89): lo que le falta no es criterio
—es `prompts/`, `corridas/`, `DECISIONES.md` con esos nombres, el análisis económico entero, el
gobierno entero, la tercera iteración y 3 corridas del sistema final. El contenido que sí tiene
(contrato de 6 piezas, proceso de 2 iteraciones, README estándar) es sólido.

## Sugerencia de mejora emitida

**D1 — hasta 22,50 puntos.** Mover el contrato a `prompts/` y las salidas a `corridas/`, crear
`DECISIONES.md`, y guardar una corrida donde `agente.html` lea una fuente de noticias real (API o
archivo) de modo que un dato de la salida sólo pueda venir de ahí. Levanta la compuerta de R1.2 y
sube D1 a nivel 3.

## Lectura

Es la corrida más útil de §5.3 hasta ahora para el **carril A**: los dos huecos de la rúbrica
(R3.3, D3 sin entradas distintas) sólo aparecen contra un repo que el grupo no diseñó. Y para el
**guion de la prueba de fuego**: si el jueves aparece un repo de Entrega 1 o 2 disfrazado de TF,
el evaluador tiene que llegar a `evaluado_con_reservas` con la duda escrita, no a un número
confiado.
