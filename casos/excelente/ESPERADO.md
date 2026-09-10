# Resultado esperado — caso excelente

> Lo que el evaluador **debe** producir con este repositorio. Es la respuesta correcta contra la
> que se compara cada corrida. Si el agente se aparta de acá, se documenta en `../../calibracion.md`.

**Puntaje esperado: en revisión · `estado: evaluado`**

> ⚠ **La banda 82–92 quedó sin respaldo el 10/9.** Una corrida limpia —sin ver este archivo—
> dio **65**, y su reserva principal era correcta: el `system_prompt.md` del caso prohibía texto
> antes del array mientras el `user_prompt.md` pedía una línea de conteo, y las tres corridas la
> traen. La contradicción la introdujimos nosotros el 31/8 y no la habíamos visto.
>
> El contrato del caso ya está corregido: la línea de conteo se declara en vez de prohibirse, y
> las corridas no se tocaron porque ya la cumplían. **Falta volver a correrlo en limpio y fijar
> la banda con el número que dé.** Hasta entonces este caso **no sirve como testigo**: un
> testigo que no da su propio valor no puede detectar deriva.
>
> Todo el episodio en `corridas/2026-09-10_el-testigo-tenia-un-defecto.md`.
>
> Lo que sigue en pie de esta corrida: **la vara separa**. Tres trabajos incompletos dieron 25,
> 26 y 25; este dio 65.

Deliberadamente **no es 100**. Un caso "excelente" que saca el máximo no prueba nada: no permite
ver si el evaluador sabe dónde falta algo en un trabajo bueno. Este trabajo tiene dos huecos
reales —la ausencia de proyección económica y sólo dos modos de falla— y el evaluador
tiene que encontrarlos.

---

## Detalle por dimensión

### D1 · Sistema completo y funcionando — nivel **4** · 30 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R1.1 | SI | Las seis piezas están y están rotuladas en `prompts/system_prompt.md`; los ejemplos son dos pares entrada→salida reales |
| R1.2 | SI | Declara el CSV del portal y las corridas traen expedientes (`EX-2026-0044178`), organismos y montos que no están en el prompt |
| R1.3 | SI | Formato especificado con 9 campos; las tres corridas devuelven los mismos 9, en el mismo orden |
| R1.4 | SI | "Nivel de delegación: L2", qué revisa (fecha de apertura y expediente) y firma con nombre y rol |

Exigencia extra de nivel 4: cumple. Los números de expediente son irreproducibles sin el archivo,
y el esquema es idéntico campo por campo en las tres corridas.

### D2 · Proceso documentado — nivel **4** · 25 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R2.1 | SI | Tres iteraciones fechadas con la tríada completa (27/8, 3/9, 4/9) |
| R2.2 | SI | Dos salidas equivocadas pegadas tal cual: `"presupuesto_oficial": 24000000` y `"presupuesto_oficial": 120` (el plazo de obra tomado como monto) |
| R2.3 | SI | Iteración 3: abandona la extracción del monto desde `descripcion`, con la razón — "preferí que me falte el dato antes que tener un dato falso" |
| R2.4 | SI | Las fechas de las iteraciones se corresponden con las de `corridas/` (3/9 y 5/9) |

Exigencia extra de nivel 4: cumple. La sección "Lo que quedó roto" cuenta una falla no resuelta y
por qué se entregó igual.

### D3 · Formato y reproducibilidad — nivel **4** · 15 pts

Los cuatro archivos exigidos, los cinco encabezados exactos del README estándar, tres corridas con
entrada / salida / fecha, y el vínculo entrada→salida verificable (el expediente de la entrada
aparece en la salida). Entradas distintas entre sí y fechadas en orden.

### D4 · Análisis económico — nivel **2** · 7,5 pts ← *el hueco principal*

| Req | Esperado | Por qué |
|-----|----------|---------|
| R4.1 | SI | 11.250 tokens de entrada y 1.100 de salida, discriminados |
| R4.2 | SI | Precio con fecha de consulta (3/9/2026) y la cuenta escrita. **El evaluador debe rehacerla**: 11.250/1M × 1,00 + 1.100/1M × 5,00 = 0,0168. Cierra |
| R4.3 | **NO** | **No hay proyección a escala.** El trabajo calcula el costo por corrida y se detiene ahí: no dice qué costaría por semana ni por año, ni declara un volumen. *(Hasta el 8/9 el caso traía una proyección de "unos 3 dólares" que no reconciliaba con la cadencia declarada en "Qué construí" — era un error accidental nuestro, no una imperfección plantada, y se quitó al cerrar D-13.)* |
| R4.4 | **NO** | "Usé el modelo liviano porque alcanza y sobra": no compara con ningún otro modelo |

### D5 · Gobierno y riesgo — nivel **3** · 11,25 pts

| Req | Esperado | Por qué |
|-----|----------|---------|
| R5.1 | SI | Lee la carpeta local (sólo lectura), escribe en una hoja específica, y dice qué **no** toca |
| R5.2 | **NO** | Sólo **dos** modos de falla. La rúbrica exige tres |
| R5.3 | SI | Concreto: verifica fecha de apertura y número de expediente contra el aviso original |
| R5.4 | SI | "Ana Beltrán, responsable de desarrollo de negocio" |

---

## Banderas esperadas

**Ninguna.** Este caso no tiene afirmaciones no verificables, ni corridas fabricadas, ni inyección,
ni relleno, ni apelación. Si el evaluador levanta una bandera acá, es un **falso positivo** y se
documenta como discrepancia.

Punto de control específico: la sección "Qué falta o qué falló" del README describe cosas que
**no** funcionan. Eso es honestidad documentada (R2.3), **no** una bandera G1. Un evaluador que
penalice a este trabajo por contar sus fallas está roto: invierte exactamente el criterio de la
materia.

---

## Aritmética

```
D1  4/4 x 30 = 30,00
D2  4/4 x 25 = 25,00
D3  4/4 x 15 = 15,00
D4  2/4 x 15 =  7,50
D5  3/4 x 15 = 11,25
             --------
bruto          88,75
penalizaciones  0,00
final              89     nota 8,9
```

## Sugerencia de mejora esperada

Debe apuntar a **D4** (la dimensión con menor proporción de puntos: 50 %) y ser accionable:
agregar la proyección a escala con su supuesto de volumen explícito (corridas por semana × semanas,
tomando la cadencia que el propio README ya declara) y correr la misma
corrida con un segundo modelo para justificar la elección con una prueba y no con una afirmación.
Potencial: hasta 7,5 puntos.
