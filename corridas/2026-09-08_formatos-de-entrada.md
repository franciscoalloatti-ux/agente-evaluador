# Verificación — el trabajo llega en formatos distintos (paso 0.5, contrato v1.6)

**Fecha:** 2026-09-08 · **Contrato:** v1.6 · **Operador:** *(completar)*

El documento de formato de la materia admite **dos** formas de entrega, textual:

> *"Todas las entregas de la materia se documentan con el mismo README, en la raíz del repositorio
> **(o del .zip)**."*

Un `.zip` casi siempre trae carpeta contenedora. Hasta la v1.5, el evaluador buscaba la estructura
obligatoria en el **nivel superior** de lo que recibía: sobre un `.zip` normal habría reportado
*"falta `README.md`, falta `prompts/`, falta `corridas/`"* sobre un trabajo que los tenía todos, un
nivel más abajo. Un falso negativo en R3.1 que hunde a alguien por una propiedad del formato que la
propia cátedra habilita, no por una decisión suya.

La v1.6 agrega el **paso 0.5 · normalización de la entrada**. Esta corrida lo verifica.

## Qué se probó

Cinco entradas construidas a partir del mismo trabajo (`casos/excelente/`), cambiando **sólo el
envoltorio**. El resultado de la estructura debería ser idéntico en las cuatro primeras.

| # | Entrada | `raiz_efectiva` esperada | R3.1 esperado |
|---|---------|--------------------------|---------------|
| 1 | Repositorio plano, estructura en el nivel superior | `.` | SI |
| 2 | Todo dentro de `trabajo-final/` | `trabajo-final` | SI |
| 3 | `.zip` extraído, contenido en `entrega-final/` | `entrega-final` | SI |
| 4 | `Prompts/` y `Corridas/` con mayúscula | `.` | SI |
| 5 | `prompt/` en singular | `.` | **NO** |

## Resultado — los cinco correctos

```
f1_repo          raiz_efectiva='.'               R3.1 = SI
f2_wrapper       raiz_efectiva='trabajo-final'   R3.1 = SI
                   observacion: carpeta contenedora, se normaliza y se reporta
f3_zip           raiz_efectiva='entrega-final'   R3.1 = SI
                   observacion: carpeta contenedora, se normaliza y se reporta
f4_mayusculas    raiz_efectiva='.'               R3.1 = SI
                   observacion: difiere en mayusculas: 'Prompts'
                   observacion: difiere en mayusculas: 'Corridas'
f5_nombre_mal    raiz_efectiva='.'               R3.1 = NO   falta prompts
```

## La línea que separa los dos casos

Los casos 4 y 5 son los que definen la regla, y conviene que quede dicho por qué no se tratan igual:

- **`Prompts/` cumple.** La diferencia de mayúsculas suele ser un artefacto del sistema operativo o
  del cliente de Git, no algo que el alumno haya decidido. Se reporta como observación y no resta.
- **`prompt/` no cumple.** El nombre en singular es una decisión, y la consigna del trabajo final es
  explícita: *"Sin excepciones de formato: el agente que te corrige no improvisa."*

Perdonar el envoltorio y no perdonar el nombre es la misma distinción que la **regla de forma y
fondo** (`rubrica.md` §0.4): se castiga lo que el alumno decidió, no lo que el formato arrastra.

## Lo que sigue sin cubrirse

- **Sin `git log` en el `.zip`.** La bandera G6 (historia de proceso falsa) no se puede verificar, y
  R2.4 se evalúa contra las fechas de las corridas. El agente lo declara en `dudas[]`; declararlo no
  lo resuelve. Es la misma reserva que ya estaba anotada para el camino B.
- **Más de dos niveles de anidamiento.** El paso 0.5 baja como máximo dos. Más abajo, la compuerta
  de D3 lo trata como incumplimiento: a esa altura el trabajo dejó de ser predecible para quien lo
  corrige, que es la razón por la que el formato es fijo.
- **Un link que no es un repositorio** (una carpeta de Drive, un documento suelto). Cae en
  `no_evaluable` si no se puede leer, o `fuera_de_alcance` si se lee y no es un trabajo final.
  Ninguno de los dos inventa una nota.

## Para el ensayo del jueves

Las cinco entradas se reconstruyen desde `casos/excelente/` cambiando sólo el envoltorio. Vale la
pena correr al menos la del `.zip` en vivo antes de la clase: es la que más probablemente aparezca,
y es la que la v1.5 rompía.
