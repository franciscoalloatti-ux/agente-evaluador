# Autocrítica — cinco cosas que la rúbrica no captura

**Fecha:** 2026-09-08 · **Contrato:** v1.7 · **Operador:** *(completar)*

Ejercicio propuesto por el profesor en la clase del 3/9, textual:

> *"Dame el cumplimiento de la rúbrica y después decirle: quiero cinco ejemplos de errores que
> podría cometer este evaluador en no capturar elementos de la rúbrica — y te da cosas que no están
> intuitivamente en la estructura de evaluación pero podrían ser relevantes."*

Es distinto de todo lo que veníamos haciendo. Las cinco rondas de calibración probaron si el
evaluador **aplica bien** los criterios que tiene. Esto pregunta **qué criterios le faltan**: dónde
un trabajo puede cumplir las veinte casillas y aun así el informe no decir lo que importa.

Los cinco están ordenados por gravedad. Los dos primeros se aplicaron hoy; los tres últimos son
decisiones que exceden a una persona y quedan planteadas.

---

## E-1 · La rúbrica no mide si el sistema **sirve** · APLICADO EN PARTE

**El error.** Las cinco dimensiones miden el **artefacto**: que exista el contrato, que haya una
herramienta, que el formato esté, que las cuentas cierren, que alguien firme. Ninguna de las veinte
preguntas es *"¿esto resuelve el problema que dice resolver?"*.

Un trabajo puede tener las seis piezas, tres corridas impecables, el costo calculado con su fuente
y el gobierno definido — y estar resolviendo un problema que no existe, o resolviéndolo mal. Sacaría
un puntaje alto.

**Por qué no lo vemos.** Es el precio de haber hecho la rúbrica ejecutable. Todo lo que exigimos es
verificable citando un archivo, y *"¿sirve?"* no se verifica citando un archivo.

**Por qué importa.** La consigna del trabajo final dice *"un sistema agéntico completo aplicado a
**un caso real** de tu trabajo, tu negocio o tu interés"*, y el profesor insiste en que los mejores
trabajos son los que resuelven un problema propio. Eso está en el enunciado y no está en nuestra vara.

**Qué se hizo.** No se agrega una dimensión: los pesos son de la cátedra y no se tocan. Se agregó a
la **exigencia extra de nivel 4 de D1** que el trabajo demuestre que el sistema *hizo algo útil*:
que alguna corrida muestre un resultado que el autor efectivamente usó, no sólo que el agente
respondió. Es lo más cerca que se puede llegar sin volver la rúbrica opinable.

**Lo que queda abierto.** Un trabajo puede seguir siendo inútil y sacar nivel 3. Es una limitación
declarada, no resuelta.

---

## E-2 · Nadie verifica que las corridas se hayan hecho **con el contrato entregado** · APLICADO

**El error.** R1.3 exige que las tres corridas compartan esquema. R3.4 exige que sean
reconstruibles. C5 cruza las fechas de las iteraciones. **Ninguno verifica que la salida guardada
se corresponda con el prompt que está en `prompts/`.**

Un trabajo puede entregar un `system_prompt.md` prolijo y tres corridas hechas con **otro** prompt
—uno anterior, uno mejor, uno de otra persona— y las veinte casillas dan igual.

**Por qué no lo vemos.** Verificamos contrato→existe y corridas→existen, cada uno contra sí mismo.
Nunca uno **contra el otro**. Es la misma clase de omisión que produjo D-13, en otra combinación.

**Qué se hizo.** Un cruce nuevo, **C7 · el contrato contra las corridas**: los campos que el
formato del contrato declara tienen que ser los que aparecen en las salidas, y las restricciones
del contrato tienen que verse cumplidas en ellas. Si el contrato fija nueve campos y las corridas
devuelven siete, o si el contrato prohíbe estimar y una salida trae un valor estimado, **las
corridas no son de ese contrato** → G7.

---

## E-3 · "Qué aprendí" es obligatorio en la materia y **ninguna dimensión lo evalúa** · APLICADO

**El error.** El formato de entrega de la materia fija cinco secciones, y la última es *"Qué
aprendí (3-5 líneas honestas: qué entendiste del trabajo con agentes haciendo esto)"*. Nuestra
rúbrica sólo comprueba que **el encabezado exista** (R3.2). Su contenido no se mira en ninguna
de las veinte casillas.

Alguien puede escribir *"aprendí mucho sobre inteligencia artificial"* y cobrar exactamente lo
mismo que quien escribe qué pieza del contrato movió el resultado y por qué.

**Por qué no lo vemos.** Cuando tradujimos la rúbrica oficial a requisitos, mapeamos cada
dimensión contra los seis requisitos del trabajo final. La sección "Qué aprendí" viene del
*formato de entrega*, que es otro documento — y se nos cayó en la juntura.

**Qué se hizo.** Se agregó a **R2.3**: además del cambio de alcance, se acepta como evidencia una
reflexión que nombre **una pieza concreta del contrato** y qué cambió al tocarla. *"Aprendí mucho"*
no cuenta; *"la pieza que más movió el resultado fue restricciones, no la tarea"* sí. Queda dentro
de D2, que es donde vive el proceso, y no inventa una dimensión nueva.

---

## E-4 · Con cincuenta trabajos, una escala de cuatro requisitos **deja de discriminar** · ABIERTO

**El error.** Cada dimensión tiene cuatro requisitos y cinco niveles. Sobre tres casos de prueba
funciona. Sobre **cincuenta trabajos reales** va a producir montones empatados: mucha gente va a
caer en el mismo nivel por razones completamente distintas, y la nota final va a agruparse en
tres o cuatro valores.

**Por qué no lo vemos.** Nunca corrimos el evaluador sobre más de cuatro repositorios. Es un
defecto que sólo aparece a escala, y la escala es exactamente lo que viene: el profesor dijo
*"va a recibir casi 50 trabajos distintos o más"*.

**Por qué importa.** Si el profesor recibe cincuenta informes y la mitad dice 68, la rúbrica no le
sirvió para lo único que necesitaba: ordenar.

**Qué haríamos.** No subir la granularidad —eso reintroduce el criterio que sacamos a propósito en
la decisión 3— sino **medir el problema antes de decidir**: correr el evaluador sobre los
repositorios públicos de compañeros que consigamos y ver la distribución real. Si se apelmaza,
la respuesta natural es un desempate **por evidencia contada** (cuántos requisitos con cita, no
cuántos niveles), no por opinión.

**Bloqueado por:** no tenemos cincuenta repositorios. Es la razón más fuerte para conseguir todos
los que podamos antes del jueves.

---

## E-5 · No hay ninguna señal sobre **quién hizo el trabajo** · ABIERTO

**El error.** D2 verifica que el proceso esté documentado y que el relato coincida con el rastro.
Pero un trabajo íntegramente generado por un agente, sin que nadie lo dirigiera ni lo revisara,
puede producir un `DECISIONES.md` perfecto: tres iteraciones, un error textual, un cambio de
alcance. Todas nuestras casillas dan verde.

**Por qué importa.** El principio de cierre de la materia es *"la responsabilidad profesional por
el output de un agente nunca se delega; el humano firma"*, y el profesor lo dijo otra vez el 3/9:
*"es importante no perder el control del armado de este agente"*. Es, literalmente, lo que el curso
quiere evitar — y nuestra rúbrica no lo ve.

**Por qué es difícil.** Detectar autoría por estilo es poco confiable y penalizaría a quien
escribe bien. Y la materia **promueve** construir con IA: el problema no es usarla, es no dirigirla.

**Qué haríamos.** No detectar autoría, sino **exigir la huella de la dirección**: que al menos una
iteración documente una decisión donde el autor **contradijo** a la herramienta — le dijo que no,
eligió lo contrario, descartó su sugerencia. Un trabajo dirigido tiene ese momento; uno generado no
lo tiene, porque no hubo nadie del otro lado.

**Está sin aplicar a propósito.** Es un cambio de criterio que afecta a los cincuenta trabajos y no
lo decide una persona sola con dos días de plazo. Va al carril A y, si hay dudas, al profesor.

---

## Lo que este ejercicio dice de nuestro propio método

Los cinco errores tienen algo en común: **ninguno se veía desde adentro de la rúbrica**. Las cinco
rondas de calibración probaron si aplicábamos bien los criterios que teníamos, y por construcción
no podían encontrar los que faltaban. Hicieron falta dos cosas de afuera para verlos —la devolución
del profesor sobre un repositorio real (H-3), la pantalla de otro grupo (v1.7)— y ahora esta
pregunta, que es la primera que dispara la revisión desde el enunciado hacia la rúbrica y no al
revés.

Vale la pena repetirlo antes de cada versión, no una sola vez.
