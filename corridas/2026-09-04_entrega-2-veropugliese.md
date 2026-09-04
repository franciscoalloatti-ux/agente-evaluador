# Corrida — repositorio real y ajeno (§5.3): `Veropugliese/entrega-2`

> Misma nota de procedencia que `entrega-1` y `entrega-3`: entrega real previa de Verónica Pugliese,
> no de un tercero. Ver la nota general en §5.3 de `calibracion.md`.

**Fecha de corrida:** 2026-09-04 · **Contrato:** v1.3 · **Camino A** (13 commits reales, 2026-08-21 a
2026-08-29).

**Resultado:** D1=1/4 · D2=1/4 · D3=0/4 · D4=0/4 · D5=2/4 · puntaje_bruto=21.25 · puntaje_final=21/100
(nota 2.1) · estado=`evaluado_con_reservas`. Sin banderas.

## Qué se rompió

1. **Mismo patrón que entrega-1 y entrega-3:** no existen `prompts/`, `corridas/` ni `DECISIONES.md`
   (el repo usa archivos en la raíz, `ejemplos/` e `iteraciones/`), lo que activa tres compuertas de
   techo simultáneas (D1≤1, D2≤1, D3≤1) pese a sustancia real: seis piezas del contrato completas, una
   corrida con datos verificables de una búsqueda real (cifra de riesgo país con fecha específica no
   trivial de inventar), dos iteraciones con tríada completa y respaldadas por commits reales a los
   4 minutos de diferencia.
2. **D5 fue la dimensión mejor lograda de los tres repos reales (nivel 2/4):** permisos explícitos de
   sólo lectura en el workflow de GitHub Actions, credenciales acotadas documentadas, y tres modos de
   falla reales con manejo (reintento con backoff en errores HTTP transitorios, descarte si Gemini no
   usó la búsqueda). Faltó sólo un punto de control humano por corrida (el único control descrito es
   puntual, al configurar el sistema) y una firma con nombre y rol.
3. **Zona gris que el agente no resolvió solo, y marcó `revision_humana_requerida: true` por eso:**
   los mensajes de commit de la automatización dicen literalmente "Preserva la entrega 1 al integrar
   la automatizacion" y la rama de origen se llama "iteracion-post-entrega-2" — sugiere que ese código
   podría no pertenecer estrictamente a "esta entrega 2", de lo que depende buena parte de D1 y D5. El
   agente usó igual el contenido como evidencia (la pasada 1 exige leer todo el repositorio) pero
   señaló la duda de atribución en vez de decidir por su cuenta.
4. **R3.2 cayó por un detalle literal:** el quinto encabezado del README es "Qué aprendí del
   contrato", no "Qué aprendí" exacto — el agente lo resolvió NO por la letra del requisito.

## Lectura

Confirma, por tercera vez con un repositorio real distinto, el mismo hallazgo estructural: las
compuertas duras escritas para el caso "no hay nada" tratan igual al caso "hay sustancia real bajo
una convención de nombres distinta". No es un defecto del agente — está aplicando la rúbrica tal como
está escrita — es un límite de diseño de la rúbrica que **no habíamos podido ver con los tres casos
construidos por el grupo**, porque los tres siguen la estructura obligatoria al pie de la letra.
