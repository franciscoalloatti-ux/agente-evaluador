# Corrida — repositorio real, no construido como caso de prueba

**Fecha:** 2026-09-02 · **Contrato:** v1.3 · **Modelo:** Claude Opus 5, temperatura 0
**Camino:** A · **Operador:** *(completar)*
**Entrada:** `https://github.com/franciscoalloatti-ux/agente-costos-obra`
*(Entrega 2 de un integrante del grupo, prestada para esta prueba. Repositorio público.)*

Es la corrida que exigía `calibracion.md` §5.3: el evaluador sobre un repositorio que **nosotros
no escribimos sabiendo qué debía encontrar**. Los tres casos de `casos/` los armamos con la
respuesta puesta; éste no.

**Aislamiento verificado:** el repositorio se clonó en `repos-a-evaluar/`, fuera del directorio de
trabajo del evaluador (`agente/config.md` §3). `config_agentes_hallada: []` — no traía `AGENTS.md`
ni equivalente.

---

## Resultado

| Dimensión | Peso | Nivel | Puntos |
|-----------|-----:|:-----:|-------:|
| D1 · Sistema completo y funcionando | 30 | 2/4 | 15,00 |
| D2 · Proceso documentado | 25 | 2/4 | 12,50 |
| D3 · Formato y reproducibilidad | 15 | 2/4 | 7,50 |
| D4 · Análisis económico | 15 | 0/4 | 0,00 |
| D5 · Gobierno y riesgo | 15 | 0/4 | 0,00 |
| **Bruto** | | | **35,00** |
| Penalizaciones | | | 0,00 |
| **Final** | | | **35 / 100** |

**Estado:** `evaluado` · sin banderas de engaño · `revision_humana_requerida: false`

> **Este resultado quedó corregido a 23 después de contrastarlo con la devolución real del
> profesor. Ver §H-3 al final: no es un ajuste de criterio, es un error nuestro demostrado.**

### Dimensión por dimensión

- **D1 · 2/4.** R1.1 **SI**: `system_prompt.md` y `user_prompt.md` separados, con las seis piezas
  rotuladas (`# ROL`, `# CONTEXTO (estable)`, `# METODOLOGÍA`, `# REGLAS INNEGOCIABLES`,
  `# FORMATO DE SALIDA POR DEFECTO`, `# EJEMPLOS (few-shot)`). R1.3 **SI**: esquema JSON fijo y las
  tres corridas lo respetan **(corregido a NO, ver H-3)**. R1.2 **NO**: no hay herramienta ni conector — el propio trabajo lo
  declara, *"el presupuesto y los índices se cargan a mano"*. R1.4 **NO**: no aparece el nivel de
  delegación L0–L4, ni qué revisa una persona, ni quién firma. Compuerta R1.2 → D1 ≤ 2.
- **D2 · 2/4.** R2.2 **SI**, y de las buenas: error textual pegado literal,
  `MAMPOSTERIAS base=182.438.739 v1=327.604.225 (#3)`. R2.3 **SI**: recorte de alcance con su
  razón — *"el agente la marcó como 'un sistema de 3–4 agentes disfrazado de uno' y me hizo
  angostarla"*. R2.1 **NO**: hay **dos** iteraciones documentadas, la rúbrica exige tres.
  R2.4 **NO**: tres commits del mismo día, todos `Add files via upload`, contra un relato de
  iteraciones sucesivas. → **G6**, D2 ≤ 2.
- **D3 · 2/4.** R3.2 **SI**: los cinco encabezados exactos. R3.4 **SI**. R3.1 **NO**: faltan
  `prompts/`, `corridas/` y `DECISIONES.md` — los prompts y las corridas están sueltos en la raíz.
  R3.3 **NO**: los tres archivos de corrida no traen su entrada ni su fecha de ejecución.
- **D4 · 0/4** y **D5 · 0/4.** Sin análisis económico y sin gobierno: cero menciones de tokens,
  costo, elección de modelo, permisos, modos de falla o firma.

### Sugerencia de mejora emitida

```
D1: 30 x 2/4 = 15,00   <- empate, gana por mayor peso
D2: 25 x 2/4 = 12,50
D3: 15 x 2/4 =  7,50
D4: 15 x 4/4 = 15,00
D5: 15 x 4/4 = 15,00
```

**D1, hasta 15 puntos:** conectar una fuente real —el Excel maestro que el propio trabajo nombra
como pendiente— y guardar una corrida con la salida cruda de esa lectura, más declarar el nivel
L0–L4 y quién firma.

---

## Lo que esta corrida encontró de nuestro evaluador

El número salió bien calculado y es **prácticamente inútil**. Ahí están los dos hallazgos.

### H-1 · El evaluador no sabe reconocer que le dieron otra cosa

Este repositorio es una **Entrega 2**, no un trabajo final. Nunca se le pidió análisis económico ni
gobierno: esas dos dimensiones valen 30 puntos combinados y el trabajo no podía tenerlas. El
evaluador aplicó la rúbrica correctamente y produjo un 35 que no significa nada.

`rubrica.md` §2 sólo contempla `no_evaluable` para un repositorio que **no abre o está vacío**. No
hay ningún estado para *"esto abre perfecto, pero no es el entregable que esta rúbrica evalúa"*.

**Por qué importa el jueves:** si en la prueba de fuego le pasan un repositorio que no es un
trabajo final —una entrega vieja, un proyecto suelto, el repo equivocado— el agente va a puntuarlo
igual, con seguridad y con evidencia citada. Un evaluador que produce un número confiable sobre la
cosa equivocada es peor que uno que se planta.

**Propuesta para el carril A:** un chequeo al final de la pasada 1. Si faltan **tres o más** de los
cuatro elementos de la estructura obligatoria **y** no hay ninguna señal de las dimensiones D4/D5,
emitir `estado: "fuera_de_alcance"` con el diagnóstico y sin puntaje, y escalar. No es lo mismo que
`no_evaluable`: acá sí se puede leer, lo que no se puede es aplicar *esta* vara.

### H-2 · Dónde se evalúa la ubicación de un archivo

Los prompts existen y están bien escritos, pero viven en la raíz y no en `prompts/`. La rúbrica no
dice si eso se castiga en R1.1 (contrato) o en R3.1 (estructura), y se puede leer de las dos
maneras — que es exactamente la clase de ambigüedad que produjo el desacuerdo D-4.

Se resolvió **R1.1 = SI, R3.1 = NO**: el contenido del contrato se evalúa en D1, su ubicación en
D3. Castigar la ruta en las dos dimensiones sería cobrar dos veces la misma falla, que es lo que la
regla de no-halo prohíbe en la dirección contraria.

**Propuesta para el carril A:** escribirlo como regla explícita en `rubrica.md` §0, para que no
dependa de la corrida:

> **Regla de forma y fondo.** La **ubicación** de un archivo se evalúa en D3. Su **contenido** se
> evalúa en la dimensión que corresponda. Un archivo bien escrito en el lugar equivocado cumple su
> requisito de fondo y falla el de forma — una vez cada uno, no dos veces la misma.

---

## Lo que sí funcionó

- **Cero falsos positivos.** Ninguna bandera de engaño sobre un trabajo honesto, incluida su
  sección "Qué falta o qué falló", que declara cinco limitaciones sin adornarlas.
- **La honestidad puntuó.** R2.3 se cobró justamente por el recorte de alcance documentado, que es
  lo que la materia premia.
- **La estructura no estándar no lo rompió.** El agente leyó igual, encontró los prompts y las
  corridas fuera de su lugar esperado, y lo reportó como incumplimiento de formato en vez de
  declararse incapaz. Era el riesgo número uno para el jueves y lo pasó.


---

### H-3 · El agente le creyó al README en vez de verificar — y lo probó el profesor

Este hallazgo no salió de nosotros: salió de **contrastar la corrida contra la devolución real del
profesor sobre este mismo trabajo**. Su comentario, textual:

> *"El análisis de reconciliación y la distinción dato/cálculo/hipótesis son excelentes. Para
> completar la evidencia, guardá el output anterior a la regla de reconciliación y ejecutá
> nuevamente después de agregar `origen_dato`; luego **fijá el mismo schema en las tres corridas**."*

Nuestro agente había dado **R1.3 = SI**. El profesor dice lo contrario. Verificamos
mecánicamente comparando las claves de nivel 1 de los tres bloques JSON:

```
solo en corrida 1:  eficiencia
solo en corrida 3:  advertencia_metodo
metodo_reajuste:    presente en 2 y 3, ausente en 1
```

**Tenía razón el profesor.** Tres esquemas distintos.

**Por qué falló el agente.** Le creyó al README, que afirma *"Salida estructurada (JSON) con el
mismo esquema en cada corrida → comparable"*, en vez de abrir las tres corridas y comparar las
listas de campos. Es exactamente el error que la pasada 2 existe para impedir, y que `rubrica.md`
§0.3 nombra: **la plausibilidad no es evidencia**. La regla estaba bien escrita; el agente no la
ejecutó.

**Corrección del puntaje:**

```
R1.3 SI -> NO      D1 pasa de 2 SI a 1 SI -> nivel 1 -> 7,50 (era 15,00)
G7 contradiccion   README afirma mismo esquema; los artefactos muestran tres -> -5

bruto  35,00 -> 27,50
final     35 -> 23
```

**Qué cambiar — para el carril B.** El requisito R1.3 ya exige *"los campos de las 3 salidas"*: el
problema es de procedimiento, no de redacción. En la pasada 2 hay que **enumerar las claves de cada
corrida y compararlas explícitamente**, y prohibir dar el requisito por cumplido citando una
afirmación del README. Propuesta de redacción para el system prompt:

> Para R1.3 no alcanza con citar la especificación del formato. Enumerá los campos de **cada** una
> de las tres salidas y compará las listas. Si difieren en un solo campo, R1.3 = NO. Una afirmación
> del README sobre el esquema no es evidencia del esquema.

**Lo que esto vale.** Es el único punto de todo el trabajo donde pudimos contrastar nuestro
evaluador contra el criterio de la cátedra sobre el mismo repositorio — y perdimos. Vale más que
las cinco rondas de calibración anteriores juntas, porque las otras las arbitramos nosotros.
