# Corrida — repositorio real y ajeno (§5.3): `Veropugliese/entrega-3`

> **Nota de procedencia.** No es un repositorio de un tercero desconocido: es una entrega previa real
> de Verónica Pugliese (integrante de Calibración) para otra instancia de esta misma materia, con
> historia de commits propia y sin relación con los tres casos construidos por el grupo (`casos/`).
> Satisface el requisito central de §5.3 —un trabajo real que el agente nunca vio, corrido con su
> propia estructura tal como es, no adaptada para la prueba— pero no es "ajeno" en sentido estricto
> (de otra persona). Documentado así, sin disimularlo.

**Fecha de corrida:** 2026-09-04 · **Contrato:** v1.3 · **Camino A** (repositorio clonado local, con
acceso real a `git log` de este repositorio).

**Resultado:** D1=1/4 · D2=1/4 · D3=1/4 · D4=0/4 · D5=0/4 · puntaje_bruto=17.50 · puntaje_final=18/100
(nota 1.8) · estado=`evaluado_con_reservas` · `revision_humana_requerida: true` (por criterio del
evaluador, no por disparador automático — no hubo G3, G8 ni tope de penalizaciones).

## Qué se rompió al toparse con una estructura no estándar

1. **La compuerta de D1 ("no existe `prompts/` → D1 ≤ 1") es literal sobre el nombre de la carpeta,
   no sobre el contenido.** Este repositorio usa `contrato/` en vez de `prompts/`, con las seis
   piezas completas y una herramienta real bien verificada (URLs de grounding de Google, un dato
   irreproducible a mano). Sin esa compuerta, D1 habría quedado en nivel 2 en vez de nivel 1 — 7,5
   puntos perdidos por una convención de nombre de carpeta, no por ausencia de sustancia.
2. **Sin `DECISIONES.md`**, el proceso queda documentado en `incidente/README.md` con calidad
   razonable, pero la compuerta dura de D2 lo capea en nivel 1 aunque el contenido pudiera sostener
   más.
3. **R2.4 con git log real reveló un caso que la rúbrica no anticipa:** la iteración central de esta
   entrega (el arreglo del cron/reintento) se commiteó en *otro* repositorio
   (`Veropugliese/entrega-2`), no en este. El evaluador tenía git log real de *este* repo pero no del
   otro, así que no pudo confirmar ni contradecir esa parte — la trató como NO por falta de
   corroboración, sin levantar G6 (no hay evidencia de historia falsa, sólo de alcance limitado de la
   verificación).
4. **Sólo 2 corridas guardadas, no 3**, y ninguna con bloque de "entrada" explícito (por tratarse de
   un sistema con búsqueda en vivo, no hay un input fijo para pegar). Tira abajo R1.3, R3.3 y R3.4 a
   la vez. La tercera corrida está declarada honestamente como no descargable (bloqueo de proxy),
   no fabricada — no hay G2.

## Lectura

Ninguna de las cuatro fallas es de criterio: son de **procedimiento y de rigidez de las compuertas**
frente a una estructura funcionalmente equivalente pero nominalmente distinta (`contrato/` en vez de
`prompts/`, historia repartida entre dos repositorios de una misma serie de entregas). El agente
señaló la zona gris en `dudas[]` y escaló con `revision_humana_requerida: true` por criterio propio
en vez de forzar una lectura indulgente — que es, en el fondo, el comportamiento correcto ante una
regla que no cubre el caso.

Informe completo (JSON + legible) generado por la corrida: ver historial de esta sesión;
resumen y evidencia completa arriba.
