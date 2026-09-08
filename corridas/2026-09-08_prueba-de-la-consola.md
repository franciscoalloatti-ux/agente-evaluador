# La consola, probada fuera del navegador

**Fecha:** 2026-09-08 · **Qué se prueba:** `front/consola.html` · **Cómo:** `node front/probar.mjs`

La consola hace tres cosas que, si fallan en silencio, arruinan un lote entero sin avisar: abrir un
`.zip`, armar el `.csv` que vuelve a Moodle, y validar el informe que devuelve el modelo. Mirar la
pantalla no alcanza para saber si las tres andan.

Así que se prueban **sin navegador**: el banco carga el JavaScript de la consola en Node con un DOM
mínimo simulado y le pasa entradas reales. Es la misma idea que le exigimos a los trabajos que
corregimos —una corrida con entrada, salida y fecha— aplicada a nuestra propia herramienta.

```
node front/probar.mjs
```

---

## Qué se le dio de comer

- **Un `.zip` armado a propósito con los cuatro casos que rompen un lector ingenuo:** archivos
  comprimidos (deflate), uno guardado **sin comprimir**, uno **binario** (una imagen), y uno de
  90.000 caracteres que **excede el tope de lectura**.
- **Una hoja de calificaciones con la cabecera real, con tildes**: `Identificador`,
  `Nombre completo`, `Dirección de correo`, `Estado`, `Calificación`,
  `Comentarios de retroalimentación`, y tres alumnos, uno de ellos sin entrega.
- **Un informe coherente** y **el mismo informe saboteado en seis lugares**.

---

## Resultado

```
27 bien, 0 mal
```

| Bloque | Qué se comprobó |
|--------|-----------------|
| **1 · el `.zip`** | Encuentra los 6 archivos · lee los comprimidos · lee el guardado sin comprimir · **omite el binario y lo dice** · **recorta el largo y lo dice** |
| **2 · el nombre de la carpeta** | De `Ana Beltran_1234567_assignsubmission_file` saca nombre e identificador. De una carpeta simple saca el nombre y **deja el identificador en nulo en vez de inventarlo** |
| **3 · la hoja** | Reconoce las seis columnas **con tildes** · `Ana Beltrán` y `Ana Beltran` son la misma persona |
| **4 · el `.csv` de vuelta** | El corregido sale con su nota · el `integridad_comprometida` sale **sin nota, con su fila intacta** · el alumno sin corregir **queda intacto** · el que no estaba en la hoja se agrega al final **marcado como `SIN IDENTIFICADOR`** · **el testigo no va al archivo** |
| **5 · la validación** | Sobre el informe sano no inventa problemas. Sobre el saboteado encuentra **los seis**: A4, A1, A5, A9, A2, y el G3 con estado incoherente, más el puntaje extremo sin `nota_al_margen` |
| **6 · el comentario** | No pasa de 180 palabras · **el número no aparece adentro del texto** |

---

## Qué pasó en la primera corrida, dicho como fue

**Pasó 27 de 27 la primera vez.** No encontró ningún error, y decirlo importa: una prueba que pasa
entera al primer intento prueba menos de lo que parece — puede estar midiendo lo que el que la
escribió ya sabía que andaba.

Lo que sí hace es **dejar clavadas dos decisiones** que son fáciles de romper sin darse cuenta la
próxima vez que alguien toque el archivo:

1. **El testigo no entra en la devolución.** `casos/excelente/` no es un alumno y no puede aparecer
   en una hoja que se importa a Moodle. Si alguien saca ese filtro, una prueba falla.
2. **Un corregido que no está en la hoja no desaparece.** Se agrega al final con
   `SIN IDENTIFICADOR` en su columna, que es feo a propósito: tiene que saltar a la vista antes de
   importar. Si alguien lo hace más prolijo y lo silencia, una prueba falla.

Su valor es ese, y es hacia adelante: es una red para el que venga, no un hallazgo de hoy.

---

## Lo que esta prueba NO prueba

- **La exportación real del campus.** El `.zip` y la hoja los armamos nosotros con el formato que
  documenta `agente/lote.md` §1, tomado del material de la materia. Que la consola se adapte a las
  columnas que encuentre reduce el riesgo, no lo elimina. Hasta correr una exportación de verdad,
  queda declarado —igual que en `agente/lote.md` §6.
- **El volumen.** Cuatro entregas en el banco, no cincuenta. Lo que se guarda en el navegador tiene
  un tope, y con lotes grandes de `.zip` la consola suelta el contenido de los archivos antes que
  perder las correcciones, y lo avisa. Ese camino está escrito pero no se ejecutó con cincuenta.
- **Que la corrección sea buena.** Esto prueba la herramienta, no la vara. La vara la prueba el caso
  testigo (`2026-09-08_ensayo-de-lote.md`), y son dos cosas distintas: se puede tener una consola
  impecable moviendo notas mal puestas.
