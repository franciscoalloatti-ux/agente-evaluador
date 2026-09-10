# El caso testigo tenía una contradicción, y la encontró el evaluador

**Fecha:** 2026-09-10 · **Contrato:** v1.11 · **Corrida limpia**, en una sesión que nunca vio
`ESPERADO.md`

---

## Cómo apareció

La pregunta que queríamos contestar era otra: **¿la vara separa un trabajo completo de uno
incompleto?** Tres proyectos de la etapa Entrega 1 habían dado 25, 26 y 25, todos apretados en el
mismo lugar, y eso olía a **E-4** — la escala que se apelmaza.

Así que corrimos `casos/excelente/` en una sesión limpia, con el `ESPERADO.md` **excluido del
paquete** para que el modelo no pudiera verlo.

| | Resultado |
|---|---|
| Los tres incompletos | **25 · 26 · 25** |
| `casos/excelente/` | **65** |

**La vara separa: dos veces y media.** Ésa era la pregunta y quedó contestada. E-4 es un problema
del medio de la tabla, no de la distancia entre tener y no tener.

Pero el testigo **cayó fuera de su propia banda** (esperado 89, banda 82–92), y su reserva principal
decía esto:

> *"El contrato tiene una contradicción: el system prompt exige sólo JSON, mientras el user prompt
> y las corridas agregan una línea antes del array."*

---

## Tenía razón

```
prompts/system_prompt.md, línea 57:  "Sin texto antes ni después del array."
prompts/user_prompt.md,   línea 12:  "Antes del array, en una sola línea, decime cuántos avisos leíste."
```

Y las tres corridas obedecen al user prompt: empiezan con `41 avisos leídos, 2 del rubro.`

**Lo pusimos nosotros el 31/8**, cuando agregamos la línea de conteo al user prompt del caso —está
registrado en su propio `DECISIONES.md`— y **nunca revisamos si chocaba con la restricción de
formato del system prompt**. Un año de cruces C7 escritos para detectar exactamente esto, y lo
teníamos adentro del caso que usamos como vara.

**Por qué no lo habíamos visto:** todas las corridas anteriores del excelente las hicimos sabiendo
qué esperábamos de él. Cuando ya sabés que un trabajo es el bueno, dejás de buscarle defectos. Es el
mismo sesgo que la puntuación a ciegas existe para evitar, aplicado a nosotros.

---

## Qué se cambió, y qué no

**Se cambió una sola cosa**, en `casos/excelente/prompts/system_prompt.md`: la restricción de
formato ahora **declara** la línea de conteo en vez de prohibirla.

```
antes:  "Sin texto antes ni después del array."
ahora:  "Antes del array va una sola línea con el conteo de lectura, en este formato exacto:
         N avisos leídos, M del rubro. Después del array, nada."
```

**Las tres corridas no se tocaron.** Ya cumplían ese formato — eran el system prompt y el user
prompt los que no se hablaban entre sí. Verificado: las tres empiezan con la línea, con el formato
exacto.

**Y esto no es acomodar el caso para que dé mejor nota.** El defecto era accidental, no plantado: si
hubiera sido una imperfección deliberada estaría en `ESPERADO.md`, y no está. La prueba es que
tampoco sabemos todavía en cuánto queda el caso — hay que volver a correrlo en limpio.

> **La regla que nos dimos, y que vale para lo que venga:** un caso se corrige cuando el defecto es
> accidental y se documenta; nunca se ajusta para llegar a un número. La diferencia es si el cambio
> se decide antes o después de mirar el resultado que uno quería.

---

## Lo que este episodio dice del evaluador

Es la segunda vez en dos días que **el agente encuentra un error nuestro que nosotros no vimos**: la
primera fue la exigencia de nivel 4 de D1, mal redactada, que tumbaba al propio testigo. Ahora una
contradicción interna dentro del caso.

En los dos casos el mecanismo fue el mismo: **el agente aplica la regla sin saber qué resultado
queríamos.** Nosotros no podemos hacer eso con nuestros propios casos, porque los escribimos.

Y hay algo más incómodo y más útil: el cruce **C7** —el contrato contra las corridas— lo escribimos
el 8/9 después del ejercicio de autocrítica, para atrapar trabajos ajenos que guardan salidas de
otro contrato. La primera vez que lo corrimos en serio sobre un caso propio, saltó.

---

## Lo que queda pendiente de esto

- **Volver a correr el caso en limpio** y fijar la banda esperada con el número que dé. Hasta
  entonces, **el testigo no es un control válido**: un testigo que no da su propio valor no puede
  detectar deriva, que es para lo único que existe.
- **Pasar el mismo cruce C7 por los otros dos casos.** Si el excelente tenía una contradicción que
  no habíamos visto, no hay razón para suponer que el flojo y el tramposo estén limpios.
