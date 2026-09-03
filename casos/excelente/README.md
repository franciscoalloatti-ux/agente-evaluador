# Radar de licitaciones — fichas de oportunidad para el estudio

## Qué construí

Un agente que revisa el listado diario de licitaciones públicas de la provincia, se queda con las
del rubro del estudio (obra civil e instalaciones), y arma una ficha corta por cada una: objeto,
organismo, presupuesto oficial, fecha de apertura y una señal de si conviene presentarse.
Lo uso yo, todos los martes y jueves a la mañana, antes de la reunión de comercial.

## Cómo se lo pedí

El contrato completo está en `prompts/`. Las instrucciones principales, en orden:

1. **System prompt** (`prompts/system_prompt.md`) — rol de analista de licitaciones, el contexto
   del estudio, la restricción central: *"si un campo no está en el aviso, devolvé `null`. Nunca
   lo estimes ni lo completes con el promedio de los otros avisos."*
2. **User prompt** (`prompts/user_prompt.md`) — la tarea por corrida: le paso el CSV exportado del
   portal de compras y le pido las fichas en JSON, con los 9 campos fijos.
3. La primera versión no tenía la restricción del `null` y el agente completaba el presupuesto
   oficial cuando el aviso no lo publicaba. Ver `DECISIONES.md`, iteración 2.

## Qué funciona

- Corre sobre el CSV que exporto del portal (`compras.provincia.gob.ar`, filtro por fecha).
  Tres corridas reales guardadas en `corridas/`, con entrada, salida y fecha.
- Devuelve JSON con los mismos 9 campos siempre: `expediente`, `organismo`, `objeto`, `rubro`,
  `presupuesto_oficial`, `moneda`, `fecha_apertura`, `senal`, `motivo_senal`.
- La ficha de cada licitación termina pegada en la hoja `radar` de mi planilla de comercial.
- El filtro por rubro anda bien: de 63 avisos del 5/9 se quedó con 4, y las 4 eran del rubro.

## Qué falta o qué falló

- **Sigue roto:** el portal publica algunos avisos con el presupuesto en el cuerpo del texto y no
  en la columna. El agente devuelve `null` (que es lo correcto según la restricción) pero eso me
  obliga a abrir el aviso a mano. Lo intenté resolver pidiéndole que lo buscara en el campo
  `descripcion` y empezó a traer números que eran plazos de obra, no plata. Preferí el `null`.
- El campo `senal` (presentarse / no presentarse / revisar) acierta cuando el objeto es claro y se
  va a `revisar` cuando el objeto es genérico ("servicios varios"). Sobre 31 fichas, 7 quedaron en
  `revisar`. No es un error, pero es más trabajo manual del que esperaba.
- No llegué a automatizar la descarga del CSV. Lo exporto a mano dos veces por semana.

## Qué aprendí

Que la pieza que más movió el resultado fue **restricciones**, no la tarea. El prompt "armame una
ficha de cada licitación" ya funcionaba; lo que lo volvió confiable fue prohibirle inventar.
También que el formato estructurado no es una decoración: cuando pasé de prosa a JSON con 9 campos
fijos, dejé de tener que leer la salida y empecé a poder pegarla en la planilla. Y que la
supervisión hay que elegirla antes, no después: puse L2 porque una licitación mal filtrada me
cuesta una semana de trabajo perdida, no un error de tipeo.

## Análisis económico

Medido sobre la corrida del 5/9 (63 avisos en el CSV):

| Componente | Tokens |
|------------|-------:|
| Contrato (system + user prompt) | 1.850 |
| CSV del día | 9.400 |
| **Entrada** | **11.250** |
| Salida (4 fichas JSON) | 1.100 |

Precio del modelo liviano consultado el 3/9/2026 en la página de precios del proveedor:
USD 1,00 por millón de tokens de entrada y USD 5,00 de salida.

```
(11.250 / 1.000.000) x 1,00 = USD 0,01125
( 1.100 / 1.000.000) x 5,00 = USD 0,00550
                     total  = USD 0,0168 por corrida
```

Redondeando, menos de dos centavos por corrida. En un año son unos 3 dólares. Usé el modelo
liviano porque para leer un CSV y llenar 9 campos alcanza y sobra.

## Gobierno y riesgo

**Qué toca.** Lee el archivo `avisos-AAAA-MM-DD.csv` de mi carpeta local (sólo lectura) y escribe
en la hoja `radar` de mi planilla de comercial (escritura, sólo esa hoja). No toca el portal de
compras, no manda mails, no publica nada.

**Qué puede salir mal.**
1. *El portal cambia el orden de las columnas del CSV.* El agente llenaría los campos cruzados.
   Mitigación implementada: el system prompt lo obliga a mapear por nombre de columna, no por
   posición, y a devolver `error_estructura` si falta una columna esperada.
2. *Un aviso sin presupuesto publicado.* El agente devuelve `null` en vez de estimarlo — es la
   restricción principal del contrato, y es la razón por la que la puse.

**Qué reviso antes de confiar.** Abro los avisos que salieron con `senal: "presentarse"` y verifico
dos cosas contra el aviso original: la fecha de apertura y el número de expediente. Si el agente
se equivoca ahí, perdemos la licitación.

**Nivel de delegación: L2 — ejecuta con revisión.** El agente arma las fichas solo; ninguna ficha
va a la reunión de comercial sin que yo la haya mirado.

**Firma:** Ana Beltrán, responsable de desarrollo de negocio del estudio.
