# Asistente de descripciones de puesto

## Qué construí

Un asistente que me ayuda a escribir las descripciones de puesto que me pide el área de RRHH.
Le paso el nombre del puesto y algunos datos y me devuelve la descripción armada, así no la
escribo desde cero cada vez.

## Cómo se lo pedí

Le escribí un prompt donde le explico que es un especialista de RRHH y le digo qué tiene que
devolver. Está en `prompts/system_prompt.md`. Después de probarlo unas veces le fui agregando
cosas, por ejemplo que responda en español, porque al principio me devolvía cosas como:

```
Job Title: Sales Representative
Reports to: Regional Sales Manager
```

y eso no me servía. Le agregué "respondé siempre en español" y se arregló.

También le puse el formato con los cinco puntos que usamos en la empresa (título, objetivo,
responsabilidades, requisitos, reporta a).

## Qué funciona

Anda bien para los puestos comerciales y administrativos, que son la mayoría de los que pido.
Las descripciones salen con los cinco puntos y las puedo pegar directo en la plantilla de RRHH.
Hice dos pruebas que están en `corridas/`.

Para puestos técnicos no lo probé.

## Qué aprendí

Que hay que ser específico con lo que uno pide. Al principio le pedía "una descripción de puesto"
y me devolvía cualquier cosa; cuando le puse los cinco puntos exactos, empezó a salir bien
siempre. También que conviene tener el prompt guardado en un archivo y no reescribirlo cada vez.

El costo no lo calculé pero debe ser muy bajo, son consultas cortas.
