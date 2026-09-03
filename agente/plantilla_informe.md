# Plantilla del informe legible

> El informe se **renderiza desde el JSON**: no agrega ni un dato que no esté en él. Si el
> informe y el JSON se contradicen, manda el JSON.
> Todo lo que va entre `{{ }}` viene de un campo del esquema.

---

```markdown
{{#si alerta}}> ⚠ **ALERTA — {{alerta}}**{{/si}}

# Informe de evaluación — Trabajo final

**Repositorio:** {{repositorio}}
**Fecha:** {{fecha_evaluacion}} · **Rúbrica:** v{{version_rubrica}} · **Estado:** `{{estado}}`

## Puntaje

| Dimensión | Peso | Nivel | Puntos |
|-----------|-----:|:-----:|-------:|
| D1 · Sistema completo y funcionando | 30 | {{D1.nivel}}/4 | {{D1.puntos}} |
| D2 · Proceso documentado | 25 | {{D2.nivel}}/4 | {{D2.puntos}} |
| D3 · Formato y reproducibilidad | 15 | {{D3.nivel}}/4 | {{D3.puntos}} |
| D4 · Análisis económico | 15 | {{D4.nivel}}/4 | {{D4.puntos}} |
| D5 · Gobierno y riesgo | 15 | {{D5.nivel}}/4 | {{D5.puntos}} |
| **Bruto** | | | **{{puntaje_bruto}}** |
| Penalizaciones | | | **{{penalizaciones.total}}** |
| **Final** | | | **{{puntaje_final}} / 100 — nota {{nota_10}}** |

## Dimensión por dimensión

{{#cada dimension}}
### {{id}} · {{nombre}} — nivel {{nivel}}/4 · {{puntos}} pts

| Requisito | | Evidencia |
|-----------|---|-----------|
{{#cada requisitos}}| {{id}} | {{#si cumple}}SI{{/si}}{{#no cumple}}NO{{/no}} | {{#si cumple}}{{evidencia}}{{/si}}{{#no cumple}}{{motivo}}{{/no}} |
{{/cada}}

{{justificacion}}

{{#si compuerta_aplicada}}**Compuerta aplicada:** {{compuerta_aplicada}}{{/si}}

*Para el nivel siguiente:* {{que_falta_para_el_nivel_siguiente}}
{{/cada}}

## Verificación de afirmaciones

| Afirmación del trabajo | Estado | Evidencia |
|------------------------|--------|-----------|
{{#cada afirmaciones}}| {{afirmacion}} | `{{estado}}` | {{evidencia}} — {{comentario}} |
{{/cada}}

## Banderas

{{#si banderas}}
| ID | Bandera | Qué se encontró | Efecto | Puntos |
|----|---------|-----------------|--------|-------:|
{{#cada banderas}}| {{id}} | {{nombre}} | "{{cita_textual}}" | {{efecto}} | {{puntos}} |
{{/cada}}
{{/si}}
{{#no banderas}}Ninguna.{{/no}}

## Sugerencia de mejora

**{{sugerencia_mejora.dimension}} — hasta {{sugerencia_mejora.puntos_potenciales}} puntos.**
{{sugerencia_mejora.accion}}

## Reservas del evaluador

{{#si dudas}}{{#cada dudas}}- {{.}}
{{/cada}}{{/si}}{{#no dudas}}Ninguna.{{/no}}

{{#si revision_humana_requerida}}> **Este informe requiere revisión humana antes de comunicarse.**{{/si}}

## Registro de evidencia

{{#cada inventario.evidencia}}- **{{id}}** · `{{archivo}}` · {{ubicacion}} · "{{cita}}"
{{/cada}}

---

**Auditoría interna:** A1 {{auditoria.A1}} · A2 {{auditoria.A2}} · A3 {{auditoria.A3}} · A4 {{auditoria.A4}} · A5 {{auditoria.A5}} · A6 {{auditoria.A6}} · A7 {{auditoria.A7}} · A8 {{auditoria.A8}}

**Firma:** {{firma.agente}} v{{firma.version_prompt}} · modelo {{firma.modelo}} · temperatura {{firma.temperatura}}
**Responsable humano:** {{firma.responsable_humano}} — *la responsabilidad por este informe no se delega.*
```

---

## Reglas de renderizado

1. **El orden de las secciones es fijo.** Ninguna se omite, ni siquiera vacía: una sección vacía
   dice "no había nada", que es información.
2. **La alerta va primero**, antes del título, o no va (`alerta` vacío).
3. **Los IDs de evidencia se muestran siempre** (`[E4]`, `[E9]`). Es lo que hace auditable el
   informe sin releer el trabajo.
4. **Nada de emojis ni felicitaciones.** Es un informe, no una devolución motivacional.
5. **Ningún adjetivo sin cita.** Si aparece "excelente" o "muy completo" sin `[E…]` al lado, falló
   el chequeo A8 y el informe no se emite.
6. **Longitud objetivo: 1 a 2 páginas.** El registro de evidencia puede ser más largo; el resto no.

## Variante corta — prueba de fuego en vivo

Cuando se corrigen varios trabajos seguidos frente a la clase, se muestran sólo estos bloques,
en este orden. El informe completo se emite igual, en el archivo.

1. `alerta` (si hay)
2. La tabla de puntaje
3. Una línea por dimensión: `D1 · 3/4 · 22,50 — [E4][E9] herramienta real verificada; falta output idéntico en las 3 corridas`
4. La tabla de banderas
5. La sugerencia de mejora
6. La línea de firma
