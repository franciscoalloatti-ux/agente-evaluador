# El día que perdimos la temperatura — y con ella el determinismo

**Fecha:** 2026-09-10 · **Contrato:** v1.10 · **Modelo:** Claude Sonnet 5 vía API
**Cómo se corrió:** `front/relay.py`, cinco corridas del mismo repositorio con el mismo contrato

Hasta hoy la prueba de estabilidad se hacía a mano, pegando el prompt y mirando el resultado. Con
el relay se puede correr sola, y lo primero que hicimos fue eso. El resultado no es el que
esperábamos y es el hallazgo más importante del día.

---

## El resultado

Cinco corridas de `github.com/franciscoalloatti-ux/pool-de-los-miercoles`, contrato idéntico:

| # | Final | Bruto | D1·D2·D3·D4·D5 | Banderas |
|---|------:|------:|----------------|----------|
| 1 | **16** | 21,25 | 1·1·0·0·2 | G1, G7 |
| 2 | **25** | 25,00 | 1·1·1·0·2 | G1 |
| 3 | **25** | 25,00 | 1·1·1·0·2 | G1 |
| 4 | **29** | 28,75 | 2·1·1·0·1 | — |
| 5 | **18** | 17,50 | 1·1·1·0·0 | — |

**Trece puntos de diferencia sobre el mismo trabajo.** No es ruido de redondeo: D1 se movió entre 1
y 2, D5 entre 0 y 2, y las banderas aparecieron en tres corridas y en dos no.

`rubrica.md` §3 exige *"puntaje idéntico, no parecido"*. Esto no lo cumple.

---

## La causa, y es concreta

La primera condición de determinismo de nuestra rúbrica es **temperatura 0**. Al llamar a la API,
el modelo la rechaza:

```
400 · `temperature` is deprecated for this model
```

**Sonnet 5 dejó de aceptar ese parámetro.** Sin él, el modelo muestrea, y muestrear es exactamente
lo que la condición prohibía.

No es un error nuestro ni un descuido: es que **el mundo se movió debajo del contrato**. La regla
seguía escrita y correcta; lo que dejó de existir es la perilla que la hacía cumplible.

El relay lo manda igual, y cuando lo rechazan **reintenta sin él y lo declara** en la respuesta
(`temperatura: null`). No lo saca en silencio: seguir firmando *"temperatura 0"* en la firma del
informe cuando no se pudo fijar sería la **G7** que penalizamos en los trabajos ajenos.

---

## Por qué esto no invalida el trabajo, y qué sí dice

**Lo que sigue en pie.** La rúbrica sigue siendo ejecutable y discutible línea por línea. Los
requisitos se siguen verificando con evidencia citada. Las banderas siguen tipificadas. Un humano
que la aplica llega al mismo número dos veces, porque la rúbrica no depende del modelo: depende de
contar requisitos.

**Lo que hay que decir de otra manera.** Hasta hoy decíamos *"dos corridas sobre el mismo
repositorio dan el mismo resultado si se cumplen siete condiciones"*. Con una de las siete fuera de
alcance, la afirmación honesta es: **el determinismo del contrato es condicional a que el modelo
permita fijar la temperatura, y hoy el modelo de gama media no lo permite.**

**Lo que hay que mirar en la dirección correcta.** La variación no está repartida al azar: se
concentra en **D1 y D5**, las dos dimensiones donde nuestros propios requisitos admiten más de una
lectura honesta. D2, D3 y D4 dieron **idénticos en las cinco corridas**. Eso no es casualidad — es
la misma señal que dio la puntuación humana a ciegas, donde Francisco y Martín difirieron
justamente en D1, D4 y D5.

> **El modelo está actuando como un quinto evaluador humano.** Y donde duda, duda en los mismos
> lugares donde dudamos nosotros. Eso convierte la inestabilidad en un instrumento de medición: nos
> dice qué requisitos están mal anclados, con una precisión que cuatro personas no alcanzan.

---

## Qué se puede hacer, ordenado por lo que cuesta

1. **Anclar D1 y D5.** Es la respuesta de fondo y no depende de ningún modelo. Si el requisito
   admite una sola lectura, la temperatura deja de importar. Es el mismo trabajo que ya pedía la
   ronda de calibración.
2. **El caso testigo, ahora con más razón.** Si la vara se mueve entre corridas, intercalar el
   testigo tres veces en el lote deja de ser una prolijidad y pasa a ser el control que decide si el
   lote se acepta o se rehace.
3. **Corregir cada trabajo más de una vez y quedarse con la mediana.** Triplica el costo —de USD 12
   a USD 36 la cursada— y no arregla la causa: la tapa. Queda anotado como opción, no como
   recomendación.
4. **Buscar un modelo que todavía acepte temperatura 0.** Probamos Haiku 4.5 y también rechazó la
   llamada. No lo perseguimos más hoy.

---

## Lo que este hallazgo NO permite decir

Que el evaluador "no sirve". Cinco corridas dieron 16, 18, 25, 25 y 29 sobre un trabajo al que dos
humanos, por separado, le pusieron 25 y 14. **La dispersión del modelo está dentro de la dispersión
humana**, y eso es un dato distinto de "es inestable": quiere decir que el problema no es el modelo,
es que la rúbrica todavía deja lugar a la interpretación en dos de sus cinco dimensiones.

Arreglar eso es el trabajo que sigue, y es el mismo con o sin API.
