# La consola — cómo se corre el evaluador

`consola.html` es un archivo suelto. **Se abre con doble click.** No hay que instalar nada, no pide
cuenta, no necesita servidor ni conexión, y no hay paso de compilación.

---

## Por qué existe, si el 2/9 la habíamos descartado

En `DECISIONES.md`, decisión 6, descartamos hacer una interfaz web: *"no aporta a ninguna de las
cinco dimensiones con las que nos corrigen"*. Eso era cierto para **nuestra nota**, y seguía sin
serlo para el trabajo del evaluador.

Lo que cambió es material de clase. El 3/9 el profesor dijo que el agente necesita una forma de
ejecución, *"y la mejor opción es un front: necesitás correr el proceso"*. Y describió el recorrido
real: Moodle le exporta las entregas, el corrector ata el nombre al repositorio, corrige en tanda y
devuelve un archivo para volver a subir.

Pero en la misma clase dijo por qué desconfía de los artefactos:

> *"Es interno de cada LLM, y por más que le des acceso a otra persona hay cosas que no puede ver o
> que no puede correr, porque tiene el sandbox con el que fue creado. Algo que te funciona
> localmente a vos puede no funcionar en otro lado."*

De ahí sale la forma: **un HTML suelto, no un artefacto.** Cualquiera lo abre, cualquiera lee su
código entero, y corre igual en cualquier máquina.

---

## La línea que no se cruza

**La consola no evalúa.**

Arma el prompt, recibe el JSON, lo valida y organiza el lote. El que corrige sigue siendo el
contrato —`agente/*` y `rubrica.md`— y sigue funcionando **en cualquier modelo, con o sin esta
pantalla**.

Si la rúbrica viviera acá adentro en JavaScript, el evaluador dejaría de ser portable y pasaría a
ser exactamente lo que el profesor señaló como problema: algo que anda donde fue construido. La
consola es el tablero, no el motor.

Por la misma razón **no embebe el contrato**: lo carga de los archivos. Si `rubrica.md` cambia, la
consola no queda vieja, y no hay dos versiones del criterio dando vueltas. Es más: si los archivos
que cargás tienen versiones distintas entre sí, la consola lo avisa antes de dejarte corregir.

---

## Está hecha para cincuenta trabajos, no para cuatro

Si ganamos la presentación, el agente no corrige al grupo: corrige **la cursada entera**. Eso cambia
la pantalla, no el criterio.

| | |
|---|---|
| **Una lista, no un desplegable** | Las entregas viven en una columna a la izquierda, con búsqueda, filtros (pendientes · corregidas · escaladas · testigos) y un punto de color por estado |
| **Se navega de a uno** | «anterior / siguiente ›» recorre lo que el filtro tenga a la vista. Con el filtro en *pendientes*, avanza sola por lo que falta |
| **Se guarda sola** | Todo queda en este navegador. Cerrás la pestaña a mitad de un lote de cincuenta y volvés donde estabas |
| **Suma, no reemplaza** | Volver a cargar la carpeta **no toca lo que ya estaba**: sólo agrega las entregas nuevas. Se puede corregir en varias sentadas |
| **Barra de avance** | Cuántos van y cuántos faltan, siempre a la vista, arriba y en la lista |

---

## Dos formas de entregar, tres de cargar

Las dos formas de entrega que existen —**link a un repositorio** y **`.zip`**— entran por cualquiera
de los tres modos:

| Modo | Cuándo se usa | Qué recibe |
|---|---|---|
| **Una por una** | La prueba de fuego, o revisar un trabajo puntual | Un nombre y una URL, o un `.zip` suelto |
| **Todas juntas** | Corregir un subconjunto: una comisión, los que faltan | Las URLs pegadas de una, o varios `.zip` a la vez |
| **El formato del campus** | La corrección real de la cursada | La carpeta de entregas: lee cada `Texto en línea.html`, saca la URL y, si la carpeta trae el identificador en el nombre, lo guarda |

**Los `.zip` se abren acá adentro.** Sin librerías y sin subirlos a ningún lado: la consola lee el
índice del archivo y descomprime con lo que el navegador ya trae. Del contenido pasa al prompt el
**árbol completo** más el texto de los archivos legibles, y **lista aparte lo que no pudo leer**
—binarios, o lo que quedó fuera del tope de lectura— para que el evaluador no puntúe sobre lo que
no vio. Es la misma regla que le exigimos a él en la pasada 1.

---

## Quién es cada uno: el ida y vuelta con Moodle

Que la corrección salga bien no alcanza si después la nota se le carga a otra persona.

- **El identificador manda.** Es lo que Moodle usa para reconocer la fila al reimportar, no el
  nombre. La consola lo saca de dos lados: del nombre de la carpeta exportada
  (`Nombre Apellido_1234567_assignsubmission_…`) y, mejor todavía, de la **hoja de calificaciones**
  que se puede cargar aparte.
- **Si cargás la hoja, la devolución sale con esa misma hoja**: la cabecera original, las filas
  originales y los identificadores originales, y sólo se completan `Calificación` y
  `Comentarios de retroalimentación`. Los alumnos que todavía no se corrigieron salen con su fila
  intacta.
- **Si no la cargás**, el `.csv` sale con identificador, nombre, calificación y comentario. Alcanza
  para pegarlo a mano, no para importarlo de una.
- **Lo que no se pudo atar, se dice.** Una corrección sin identificador sale igual en el archivo,
  pero la consola la lista antes de que descargues nada. **No se adivina de quién es un trabajo.**
- **La nota y el texto van separados.** El puntaje en su columna, la devolución en la suya. El
  número nunca va adentro del texto: quedaría duplicado en la pantalla del alumno.

Los estados sin nota —`integridad_comprometida`, `fuera_de_alcance`, `no_evaluable`— salen con la
**columna de calificación vacía a propósito**, y se listan aparte para que una persona los lea antes
de importar nada.

---

## Las seis pantallas

| | Qué hace |
|---|---|
| **Corrección** | Tres columnas: las entregas, el trabajo (prompt · respuesta · informe · entregable) y el panel de corrección |
| **Métricas** | Cuántos van, promedio, mediana, mínimo y máximo, desvío, distribución, nivel promedio por dimensión, estados y banderas |
| **Lote y testigos** | El control: si los testigos coinciden entre sí y con su valor esperado, la vara no se movió |
| **Devolución** | La hoja para Moodle, la vista rápida y la lista de escalados |
| **Cargar** | El contrato, las tres formas de cargar entregas, la hoja de calificaciones y el caso testigo |
| **Qué es esto** | Los límites, escritos donde el que la usa los lee |

### Las métricas describen, no evalúan

Son sobre el lote ya corregido y **ninguna entra en ninguna nota**. Si la distribución del lote
pudiera mover un puntaje, el puntaje dejaría de depender del trabajo — que es exactamente el error
que la regla de no-anclaje de `rubrica.md` §1 existe para impedir.

Sí sirven para una cosa: cuando el desvío se achica y todos caen en la misma franja, la consola lo
dice y lo nombra —**E-4** de la autocrítica, *la escala se apelmaza con volumen*—. Es un problema
conocido y declarado, y vale decirlo antes de que lo diga otro.

---

## Lo que valida al recibir un informe

No es decorativo: son los chequeos de la pasada 4, hechos **fuera del modelo**, que es donde no
puede autoengañarse.

| | Qué comprueba |
|---|---|
| **Esquema** | Los campos exigidos están |
| **A1** | Ningún requisito en `SI` sin evidencia citada |
| **A2** | Toda cita apunta a un ID que existe en el inventario |
| **A4** | El nivel coincide con la cuenta de requisitos cumplidos |
| **A5** | `nivel × peso` cierra en las cinco, y el bruto es su suma |
| **A9** | Los siete cruces reportados. Uno sin reportar es indistinguible de uno no hecho |
| **Integridad** | Si hay banderas G3, el estado tiene que ser `integridad_comprometida` y el final 0 |
| **Nota al margen** | Un puntaje extremo (< 40 o > 90) sin `nota_al_margen` se marca |

**Probado, no supuesto.** Hay un banco de 27 pruebas que corre sin navegador
(`corridas/2026-09-08_prueba-de-la-consola.md`): abre un `.zip` real —con archivos comprimidos, uno
sin comprimir, uno binario y uno recortado por largo—, lee una hoja de calificaciones con tildes,
produce el `.csv` de vuelta y lo verifica fila por fila, y le pasa a `validar()` un informe sano y
uno saboteado en seis lugares. Los seis los encuentra.

---

## Lo que no hace, dicho de frente

- **No llama al modelo.** Copiás el prompt y pegás la respuesta. Automatizarlo pediría una API key
  metida en el navegador, y una credencial no se pone donde no hace falta. Es el mismo criterio con
  el que penalizamos la G8 en los trabajos que corregimos.
- **No sube nada a Moodle.** Produce el archivo; lo importa una persona. El mismo límite que tiene
  el evaluador con el repositorio que corrige.
- **No adivina de quién es un trabajo.** Si no hay identificador o no hay nombre, la fila sale
  marcada y la ata una persona.
- **De un `.zip` lee texto, no binarios.** Una captura de pantalla o un `.xlsx` aparecen en el árbol
  con su tamaño, pero su contenido no se lee, y eso va escrito en el prompt.
- **No se probó contra una exportación real del campus.** El formato está tomado del material de la
  materia y la consola se adapta a las columnas que encuentre, pero hasta que no corramos una
  exportación de verdad esto queda declarado como pendiente, igual que en `agente/lote.md` §6.

---

## Nada sale de tu máquina

No hay una sola llamada de red en todo el archivo. Los archivos —incluidos los `.zip`— se abren en
el navegador, los resultados se arman ahí y el `.csv` se genera ahí. Lo corregido se guarda en este
navegador y en ningún otro lado. La consola nunca ve una credencial porque nunca necesita ninguna.
