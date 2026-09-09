# Corrida — repositorio real (§5.3): `federicobofer/analisisconsumos`

> **Nota de procedencia.** Repositorio real de Federico Böfer de la etapa de la Entrega 1
> (4 commits del 2026-08-20), nunca visto antes por el agente. Misma reserva que el resto de §5.3.

**Fecha de corrida:** 2026-09-08 · **Contrato:** v1.10 · **Camino A** (clon aislado en `~/re/ac`).

**Resultado:** `estado` = `fuera_de_alcance` · **sin puntaje** · `revision_humana_requerida` = true.
**Es el primer caso real que dispara `fuera_de_alcance`.**

## Inventario

- `config_agentes_hallada`: `[]`.
- `raiz_efectiva`: `.` — `formato_entrada`: `repositorio_git`.
- Archivos raíz: `README.md` (5 líneas, **no es el README estándar**), `Agente Claude` (un archivo
  con una sola línea: un link `claude.ai/share/...`).
- Estructura obligatoria: **0 de 4**. No hay `prompts/`, `corridas/` ni `DECISIONES.md`.
- El sistema descrito ("analiza consumos de tarjeta, compara períodos, sugiere eficiencias") **no
  está en el repositorio**: vive en una conversación de Claude enlazada, que el evaluador no puede
  abrir. Los "archivos principales" que menciona el README (resúmenes de tarjeta) no están
  versionados.
- Commits: 4, todos del 2026-08-20 ("Initial commit", "Agente", "Update README.md" ×2).

## Por qué `fuera_de_alcance` y no `no_evaluable` ni una nota

`system_prompt.md` pasada 1, punto 6: faltan **tres o más** de los cuatro elementos de la
estructura obligatoria **y** no hay **ninguna señal de D4** (tokens, costo, elección de modelo)
**ni de D5** (permisos, modos de falla, firma con rol). Se cumplen las dos condiciones.

- No es `no_evaluable`: el repositorio **abre y se lee perfecto**. Lo que no se puede es aplicar
  *esta* vara.
- No se emite un número: sería *"un número confiable sobre la cosa equivocada, que es peor que no
  dar ninguno"* (`plantilla_informe.md`).

`"Alumno: Böfer Federico"` es una firma de entrega, no la firma de un responsable de sistema con
rol que exige R5.4 — no cuenta como señal de D5.

## Qué se rompió

1. **Nada se rompió en el evaluador: el estado `fuera_de_alcance` funcionó como está diseñado.**
   Es la primera vez que se ejerce contra un repo real. La compuerta escrita en la v1.5 —y no
   probada sobre un caso que la active, según `calibracion.md` §8 y `DECISIONES.md`— quedó
   verificada.

2. **El límite real es la conversación enlazada.** Un porcentaje de las entregas de esta materia
   va a apuntar a un `claude.ai/share/...` en vez de traer el sistema al repo. El evaluador no
   tiene forma de seguir ese link, y el estado correcto es `fuera_de_alcance` con el diagnóstico
   —no `no_evaluable`, porque el repo sí abre—. Conviene que el **guion de la prueba de fuego**
   contemple este caso.

## Lectura

Cierra un pendiente declarado: la compuerta `fuera_de_alcance` tenía redacción y no evidencia.
Ahora tiene una corrida real que la ejerce. Para la prueba de fuego: si aparece un repo así, el
evaluador dice *"esto abre y se lee perfecto, pero no es un trabajo final"*, enumera lo que falta,
y lo manda al profesor sin inventar un número.
