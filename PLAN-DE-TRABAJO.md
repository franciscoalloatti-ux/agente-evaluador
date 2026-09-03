# Plan de trabajo del grupo

> El parcial evalúa el **proceso grupal** con peso 15: historia de commits, iteraciones de la
> rúbrica, decisiones registradas. *"Un repo con un único commit del último día cuenta una historia
> — y no es buena."*
>
> **Este archivo es el plan, no la evidencia.** La evidencia la producen ustedes commiteando.

---

## Advertencia, y va en serio

**No fabriquen la historia de commits.** No antedaten, no repartan commits ajenos entre los cuatro
usuarios, no armen una secuencia falsa el 9 a la noche.

Dos razones. La primera es que se nota: nuestro propio agente tiene una bandera para eso (**G6**,
historia de proceso falsa) y el evaluador que corrija este parcial probablemente tenga la suya. La
segunda es peor: sería usar el caso tramposo como manual de instrucciones, en el mismo repositorio
donde escribimos que eso no se hace.

Cuatro días de commits reales de cuatro personas cuentan una historia mucho mejor que veinte
commits inventados. Si algo lo hizo una sola persona, que el commit lo diga.

---

## Reparto por carriles

Cuatro carriles que casi no se pisan, así se puede trabajar en paralelo sin conflictos.

| Carril | Dueño | Archivos | Qué implica |
|--------|-------|----------|-------------|
| **A · Rúbrica** | *(integrante 1)* | `rubrica.md` | Es la pieza de mayor peso (25 del parcial). Cada requisito tiene que poder responderse sí/no citando evidencia. Si un requisito necesita interpretación, está mal escrito |
| **B · Agente** | *(integrante 2)* | `agente/*` | El contrato, el esquema de salida, la plantilla y las banderas. Dueño también del determinismo: si dos corridas difieren, es de este carril |
| **C · Casos** | *(integrante 3)* | `casos/*` | Los tres mini-repos y sus `ESPERADO.md`. El carril más divertido y el más importante: sin un tramposo difícil, el evaluador no se prueba |
| **D · Calibración** | *(integrante 4)* | `calibracion.md`, `corridas/` | Corre el agente, compara contra `ESPERADO.md`, documenta los desacuerdos. **No cambia la rúbrica: la discute.** Quien la cambia es el carril A |

**Regla de conflicto:** nadie edita el archivo de otro carril. Si el carril D encuentra un problema
en la rúbrica, abre un issue o lo comenta en `calibracion.md`; lo cambia el carril A. Así el
`git log` muestra quién decidió qué, que es exactamente lo que se evalúa.

---

## Secuencia sugerida hasta el 10/9

Cada línea es al menos un commit. Los mensajes tienen que decir **qué decidieron**, no "cambios".

### Antes que nada — cada uno, un commit propio

1. **(los cuatro)** Cada integrante completa su fila de la tabla del README y commitea **su propia
   línea**. Cuatro commits, cuatro autores, el primer día. Es la forma más barata de que el
   `git log` muestre desde el arranque que el grupo existe.

### Día 1 — arranque

2. **A** — `rubrica.md`: revisar los 20 requisitos. Para cada uno preguntarse: *¿puedo responder
   sí o no citando un archivo?* Los que no pasen, reescribirlos.
   → commit: `rubrica: reescribo R2.4 y R5.2, no se podían responder sin interpretar`
3. **B** — leer `agente/system_prompt.md` entero y **correrlo** una vez sobre el caso excelente.
   → commit: `agente: primera corrida propia, guardo la salida cruda`
4. **C** — leer los tres casos. Decidir si el tramposo es **lo bastante difícil**. Tiene seis
   vectores; pensá un **séptimo** de una clase que todavía no esté cubierta.
   → commit: `casos: sumo un septimo vector de inyeccion en la salida de una corrida`

### Día 2 — calibración a ciegas (§5.1 de `calibracion.md`)

5. **(los cuatro, en paralelo y sin hablarse)** Cada uno puntúa los tres casos dimensión por
   dimensión, **sin abrir** `ESPERADO.md` ni `corridas/`. Cada uno commitea su columna.
   → cuatro commits: `calibracion: cargo mi puntuación a ciegas`
6. **D** — juntar las cuatro columnas y marcar los desacuerdos. **Buscar primero los
   humano-vs-humano**: si dos integrantes puntúan distinto la misma dimensión, la rúbrica no está
   lo bastante anclada, y eso vale más que cualquier coincidencia con el agente.
   → commit: `calibracion: 3 desacuerdos humano-humano en D2 y D5`
7. **A** — ajustar `rubrica.md` a v1.2 con lo que salió. Actualizar la tabla de versiones.
   → commit: `rubrica v1.2: anclo R2.1 tras el desacuerdo D-7`

### Día 3 — estabilidad y repo ajeno

8. **B** — prueba de estabilidad: tres corridas de cada caso, sesiones limpias.
   → commit: `corridas: prueba de estabilidad, 3x3, puntajes idénticos`
9. **C o D** — conseguir **un repositorio real y ajeno** (la Entrega 1 o 2 de alguien que preste el
   suyo) y correr el agente encima. **Es la prueba que más va a parecerse a la del jueves.**
   → commit: `corridas: primer repo ajeno, se rompió al leer un README sin encabezados`
10. **A/B** — arreglar lo que se rompió. Subir versión.
    → commit: `agente: manejo de README sin la estructura estándar`

### Día 4 — cierre

11. **B** — completar el cuadro de costos de `agente/config.md` §4 con precios **consultados y
    fechados**. Es la deuda declarada en el README y se cierra en veinte minutos.
    → commit: `config: precios consultados el 9/9, costo por corrida calculado`
12. **D** — cerrar `calibracion.md` §5 con las tablas llenas.
    → commit: `calibracion: ronda 3 completa`
13. **(todos)** — releer el README: que "Qué falta o qué falló" siga siendo cierto después de todos
    los arreglos. Que no quede prometiendo algo que ya no falta, ni escondiendo algo que sí.
    → commit: `readme: actualizo lo que falta tras la ronda 3`

---

## Ensayo de la prueba de fuego

**Hacerlo una vez, antes del jueves.** Uno del grupo consigue un repositorio que los otros tres no
vieron, y el agente lo corrige en vivo, con reloj.

Qué mirar:
- **Cuánto tarda.** Si tarda más de lo que dura la atención de un aula, hay que recortar la salida
  a la variante corta de `agente/plantilla_informe.md`.
- **Qué pasa si el repo no abre.** Debe salir `estado: "no_evaluable"`, no una nota inventada.
  Probarlo a propósito con una URL rota.
- **Qué pasa si el repo no tiene la estructura estándar.** Es el caso más probable en vivo.
- **Quién habla.** El informe se lee, no se improvisa. Si alguien tiene que explicar el puntaje con
  palabras propias, el informe no estaba bien escrito.

Llevar el contrato en un archivo listo para pegar, no en cuatro pestañas.

---

## Checklist de entrega — jueves 10/9, 18:59

- [ ] Repositorio **público** en GitHub, y **abierto en una ventana de incógnito** para
      confirmarlo. Un repo privado es `no_evaluable`, y esa lección la escribimos nosotros
- [ ] El repositorio evaluado se clona **fuera** del directorio de trabajo del evaluador, y el
      informe declara `config_agentes_hallada`. Si ese campo viene vacío en un repo que tiene un
      `AGENTS.md`, el agente no lo buscó
- [ ] `README.md` con las cinco secciones estándar + la tabla de integrantes completa
- [ ] `rubrica.md`, `agente/`, `casos/excelente|flojo|tramposo/`, `calibracion.md` — los nombres
      exactos de la consigna
- [ ] `git log` con commits de los cuatro integrantes, repartidos en el tiempo
- [ ] Las tablas de `calibracion.md` §5 llenas, o dicho explícitamente qué no se llegó a hacer
- [ ] El cuadro de costos de `agente/config.md` §4 con precios y fecha de consulta
- [ ] Ensayo de la prueba de fuego hecho al menos una vez
- [ ] Un integrante sube el link en la actividad **Parcial** del campus
