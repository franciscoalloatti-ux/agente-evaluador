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

## Las cinco pantallas

| | Qué hace |
|---|---|
| **1 · Contrato** | Cargás los cuatro archivos. Muestra la versión de cada uno y **avisa si no coinciden entre sí** |
| **2 · Cargar trabajos** | Tres modos: la carpeta `Entregas/` de Moodle (lee los `Texto en línea.html` y saca las URLs), URLs pegadas a mano, o el caso testigo intercalado |
| **3 · Corregir** | Arma el prompt exacto, lo copiás, lo corrés donde quieras, y pegás el JSON de vuelta |
| **4 · Lote y testigos** | El control: si los testigos coinciden entre sí y con su valor esperado, la vara no se movió |
| **5 · Devolución** | La hoja para Moodle (.csv) o la vista rápida, y la lista de escalados |

---

## Lo que valida al recibir un informe

No es decorativo: son los chequeos de la pasada 4, hechos **fuera del modelo**, que es donde no
puede autoengañarse.

| | Qué comprueba |
|---|---|
| **Esquema** | Los campos exigidos están, y en orden |
| **A1** | Ningún requisito en `SI` sin evidencia citada |
| **A2** | Toda cita apunta a un ID que existe en el inventario |
| **A4** | El nivel coincide con la cuenta de requisitos cumplidos |
| **A5** | `nivel × peso` cierra en las cinco, y el bruto es su suma |
| **A9** | Los siete cruces reportados. Uno sin reportar es indistinguible de uno no hecho |
| **Integridad** | Si hay banderas G3, el estado tiene que ser `integridad_comprometida` y el final 0 |
| **Nota al margen** | Un puntaje extremo (< 40 o > 90) sin `nota_al_margen` se marca |

Probado contra un informe real de la v1.3 —detectó que le faltaban los campos nuevos y los siete
cruces— y contra uno saboteado a propósito en cinco lugares: los encontró todos.

---

## Lo que no hace, dicho de frente

- **No llama al modelo.** Copiás el prompt y pegás la respuesta. Automatizarlo pediría una API key
  metida en el navegador, y una credencial no se pone donde no hace falta. Es el mismo criterio con
  el que penalizamos la G8 en los trabajos que corregimos.
- **No abre `.zip`.** Para el trabajo final no hace falta: la entrega es un link a un repositorio y
  el índice sale de los `Texto en línea.html`. Si algún día llega un `.zip`, se descomprime a mano.
- **No sube nada a Moodle.** Produce el archivo; lo importa una persona. El mismo límite que tiene
  el evaluador con el repositorio que corrige.
- **No adivina de quién es un trabajo.** Si no hay URL o no hay nombre, la fila sale marcada y la
  ata una persona.

---

## Nada sale de tu máquina

No hay una sola llamada de red en todo el archivo. Los archivos se leen en el navegador, los
resultados se arman ahí y el `.csv` se genera ahí. La consola nunca ve una credencial porque nunca
necesita ninguna.
