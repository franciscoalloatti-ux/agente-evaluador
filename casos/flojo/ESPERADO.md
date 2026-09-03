# Resultado esperado — caso flojo

> Lo que el evaluador **debe** producir con este repositorio.

**Puntaje esperado: 18 / 100 (rama severa) o 21 (rama indulgente) · banda aceptable 15 – 30 · `estado: evaluado`**

Este caso es un trabajo **real pero incompleto**: alguien que efectivamente construyó algo chico y
lo documentó mal. No es un tramposo. La prueba que corre acá es que el evaluador **puntúe bajo sin
levantar banderas**: no hay nada que castigar más allá de lo que falta.

Un evaluador que le pone 55 a este trabajo está inflando. Uno que le pone 0 está confundiendo
*incompleto* con *fraudulento*, y esa confusión es peor: destruye la señal que separa al flojo del
tramposo.

---

## Detalle por dimensión

### D1 · Sistema completo y funcionando — nivel **1** · 7,5 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R1.1 | **SI** | Existen los dos archivos y se identifican cinco de las seis piezas: rol ("especialista en Recursos Humanos"), contexto (la empresa de 180 empleados), tarea, restricciones ("no inventes el rango salarial"), formato (los cinco puntos). Falta **ejemplos** — una sola pieza, y la rúbrica exige que falten dos o más para dar NO |
| R1.2 | **NO** | No hay herramienta ni conector: el usuario tipea el nombre del puesto y pega la respuesta a mano. Nada en las corridas proviene de una fuente externa |
| R1.3 | **NO** | El formato está especificado, pero hay **dos** corridas, no tres. La rúbrica exige que las tres lo respeten |
| R1.4 | **NO** | No se menciona nivel de delegación, ni qué revisa una persona, ni quién firma |

**Compuerta aplicada:** R1.2 = NO → D1 ≤ 2. El nivel base ya era 1, así que la compuerta no lo baja.

### D2 · Proceso documentado — nivel **1** · 6,25 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R2.1 | **NO** | No hay iteraciones documentadas con la tríada. El README menciona que "le fue agregando cosas", sin fechas ni secuencia |
| R2.2 | **SI** | Hay un error textual pegado tal cual: `Job Title: Sales Representative / Reports to: Regional Sales Manager` — la salida en inglés que motivó el cambio |
| R2.3 | **NO** | Nada descartado, achicado ni pospuesto con su razón. "Para puestos técnicos no lo probé" es una limitación, no una decisión de alcance registrada |
| R2.4 | **NO** | No hay `DECISIONES.md` ni fechas contra las cuales cruzar nada. Las corridas tampoco están fechadas |

**Compuerta aplicada:** no existe `DECISIONES.md` → D2 ≤ 1.

### D3 · Formato y reproducibilidad — nivel **1** · 3,75 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R3.1 | **NO** | Falta `DECISIONES.md` en la raíz |
| R3.2 | **NO** | El README tiene cuatro de las cinco secciones. Falta **"Qué falta o qué falló"** |
| R3.3 | **NO** | Dos corridas, y **ninguna con fecha** |
| R3.4 | **SI** | Las dos corridas que hay sí son reconstruibles: la entrada está completa y el puesto pedido aparece en la salida |

**Compuerta aplicada:** menos de 3 corridas → D3 ≤ 1.

### D4 · Análisis económico — nivel **0** · 0 pts

Los cuatro requisitos en NO. La única mención es *"El costo no lo calculé pero debe ser muy bajo"*,
que es exactamente el ancla de nivel 1 de la rúbrica sin siquiera el número.

### D5 · Gobierno y riesgo — nivel **1** · 3,75 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R5.1 | **NO** | No hay inventario de sistemas ni permisos |
| R5.2 | **NO** | Ningún modo de falla identificado |
| R5.3 | **SI** | *"las puedo pegar directo en la plantilla de RRHH"* precedido de la revisión implícita — **atención, punto de duda**: ver más abajo |
| R5.4 | **NO** | Nadie firma |

**Compuerta aplicada:** R5.4 = NO → D5 ≤ 2.

> ### Punto de duda deliberado — R5.3
> Este requisito es discutible y está puesto a propósito. El trabajo **no** dice explícitamente
> "reviso X antes de confiar"; dice que las descripciones "las puede pegar directo". Un evaluador
> estricto lee eso como ausencia de control y marca **NO** (D5 cae a nivel 0 y el total a **18**).
>
> **La respuesta correcta según `rubrica.md` §0.4 es la más severa: R5.3 = NO**, porque la regla de
> desempate manda al nivel menor y la evidencia exigida es *"qué revisa la persona antes de confiar
> en la salida, en concreto"*, que acá no está.
>
> Si el agente devuelve **18**, es correcto y no es una discrepancia.
> Si devuelve **21** marcando R5.3 = SI, tiene que aparecer en `dudas[]`; si no aparece, **sí** es
> una discrepancia: significa que resolvió una ambigüedad sin registrarla.
>
> Los dos resultados caen dentro de la banda. Lo que se evalúa acá no es el número: es si el
> evaluador **sabe que dudó**.

---

## Banderas esperadas

**Ninguna.** En particular:

- *"El costo no lo calculé pero debe ser muy bajo"* → **no** es G1. No afirma haberlo calculado:
  admite que no lo hizo. Es honestidad, y ya está castigada por vía del puntaje (D4 = 0).
- *"Para puestos técnicos no lo probé"* → **no** es G1 por la misma razón.
- El README es corto → **no** es G4. La brevedad no es relleno; el vacío sí, y acá no hay secciones
  vacías con título grandilocuente.

Un evaluador que levanta banderas en este caso está castigando dos veces lo mismo.

---

## Aritmética

```
D1  1/4 x 30 =  7,50
D2  1/4 x 25 =  6,25
D3  1/4 x 15 =  3,75
D4  0/4 x 15 =  0,00
D5  1/4 x 15 =  3,75   (0,00 si R5.3 = NO -> bruto 17,50 -> final 18)
             --------
bruto          21,25
penalizaciones  0,00
final              21     nota 2,1
```

## Sugerencia de mejora esperada

Regla del system prompt: `puntos_recuperables = peso × (4 − nivel) / 4`.

```
D1: 30 x 3/4 = 22,50   <- mayor
D2: 25 x 3/4 = 18,75
D3: 15 x 3/4 = 11,25
D4: 15 x 4/4 = 15,00
D5: 15 x 3/4 = 11,25
```

La sugerencia debe apuntar a **D1**, con hasta **22,5 puntos** potenciales, y debe ser concreta:
conectar una fuente real —por ejemplo, que el agente lea la planilla de puestos existentes en vez
de recibir el nombre tipeado— y guardar una tercera corrida con fecha. Es lo que levanta la
compuerta R1.2 y desbloquea el resto de la dimensión.

*(Nota de diseño: la regla mecánica "la dimensión más baja" habría apuntado a D4, que tiene 0
puntos pero sólo 15 de peso. La fórmula de puntos recuperables apunta a D1, que es donde está el
problema real de este trabajo. Este caso es el que nos hizo cambiar la regla — ver
`../../calibracion.md`, discrepancia D-2.)*
