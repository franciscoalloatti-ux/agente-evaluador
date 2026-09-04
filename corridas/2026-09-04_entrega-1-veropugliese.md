# Corrida — repositorio real y ajeno (§5.3): `Veropugliese/entrega-1`

> **Nota de procedencia.** Igual que `entrega-3`: es una entrega real previa de Verónica Pugliese
> para otra instancia de la materia, no de un tercero. Real y fuera de muestra, no "ajena" en
> sentido estricto — ver la nota general en §5.3 de `calibracion.md`.

**Fecha de corrida:** 2026-09-04 · **Contrato:** v1.3 · **Camino A** (7 commits reales, 2026-08-16 a
2026-08-21).

**Resultado:** D1=1/4 · D2=1/4 · D3=1/4 · D4=0/4 · D5=1/4 · puntaje_bruto=21.25 · puntaje_final=21/100
(nota 2.1) · estado=`evaluado_con_reservas`.

## Qué se rompió

1. **La estructura obligatoria (`prompts/`, `corridas/`, `DECISIONES.md`) nunca existió**, confirmado
   con `git log --all --name-only` sobre los 7 commits (no por inferencia). Esto activa **tres
   compuertas de techo simultáneas** (D1≤1, D2≤1, D3≤1) que aplastan el puntaje sin importar la
   sustancia real debajo. D2 es el caso más flagrante: por conteo de requisitos cumplidos (3 de 4,
   con dos iteraciones corroboradas por commits reales) sacaría nivel 3 — y termina en nivel 1 sólo
   porque el archivo se llama distinto de lo esperado.
2. **R1.2 fue la decisión más difícil de la corrida.** La rúbrica pide citar el dato de la
   herramienta real "en `corridas/`", que no existe acá. El agente tuvo que decidir si el requisito
   vive en el concepto (herramienta real + dato verificable) o en la ubicación literal del archivo.
   Resolvió que vive en el concepto, apoyado en evidencia fuerte (consistencia aritmética cruzada en
   9 series de precios + un desfasaje de 13 minutos entre el timestamp embebido en la página y el
   commit real que lo sube — un dato que el modelo no pudo inventar). Con la lectura más estricta de
   la letra, R1.2 sería NO y el puntaje final bajaría de 21 a 14. Es el punto de menor
   reproducibilidad de esta corrida.
3. **Hallazgo sin bandera tipificada:** el README conserva, en el commit final, una nota dirigida al
   alumno pidiéndole personalizar la sección "Qué aprendí" antes de entregar — sugiere que ese
   párrafo no fue revisado. No es G3 (no apunta al evaluador) ni G4 (el resto tiene contenido real).
   El agente lo registró en `dudas[]` sin tocar el puntaje, por no tener dónde tipificarlo.
4. **Dato de identidad no usado para nada:** uno de los emails de autoría en `git log`
   (`verop483@gmail.com`) coincide con el email asociado a la sesión de evaluación. El agente lo
   señaló por transparencia y explícitamente no lo usó para ablandar ni endurecer el criterio — el
   trabajo se evaluó como anónimo, tal como pide el contrato. Validación práctica útil de la
   restricción "no compares alumnos / tratá al alumno como anónimo".

## Lectura

Mismo patrón que `entrega-3`: las compuertas duras, escritas para castigar la ausencia real de
estructura, no distinguen entre "no hay nada" y "hay sustancia real bajo un nombre de carpeta
distinto". Es el `D-7`/`D-8` de la ronda 4 pero aplicado por primera vez a un repositorio que el
grupo no diseñó — la señal es más creíble por eso mismo.
