# La rúbrica contra la consigna — ¿medimos lo que el trabajo final pide?

**Fecha:** 2026-09-08 · **Contrato:** v1.9 → **v1.10** · **Fuente:** los dos PDF de la cátedra
(`Trabajo final — Un sistema agéntico para un caso real` y `Parcial — El agente evaluador`)

Hasta hoy verificamos que el evaluador fuera **estable** (mismo trabajo, mismo número), **consistente**
(el trabajo 50 con la misma vara que el 1) y **resistente** (los ocho vectores del tramposo). Nunca
verificamos lo más básico: que lo que medimos sea **lo que la consigna pide**.

Este es ese cruce, en la dirección que importa: **de la consigna hacia la rúbrica**. Al revés
—mirar nuestros requisitos y buscarles justificación— sólo confirma lo que ya escribimos.

---

## Los seis requisitos del trabajo final, uno por uno

| # | Lo que pide la consigna | Dónde se mide | ¿Cubierto? |
|---|-------------------------|---------------|-----------|
| **1** | **Objetivo claro** | — | **NO** ← el hallazgo |
| 1 | Contrato escrito (system + user, con las seis piezas) | R1.1 | Sí |
| 1 | Al menos una herramienta o conector real | R1.2 | Sí, y con la exigencia de un dato irreproducible sin ella |
| 1 | Salida en formato estructurado | R1.3 | Sí, enumerando los campos de las tres corridas |
| 1 | Supervisión humana definida con L0–L4 | R1.4 | Sí |
| **2** | Tres corridas reales, guardadas tal como salieron | R3.3 · G2 | Sí |
| 2 | Reconstruibles por un tercero | R3.4 | Sí |
| 2 | Con **entradas reales** | R3.4 + nivel 4 de D3 | Parcial — ver abajo |
| **3** | Estructura obligatoria: `README.md`, `prompts/`, `corridas/`, `DECISIONES.md` | R3.1 | Sí, con raíz efectiva |
| 3 | README estándar de la materia | R3.2 | Sí, los cinco encabezados |
| **4** | `DECISIONES.md`: iteraciones, errores textuales, cambios de alcance | R2.1 · R2.2 · R2.3 · R2.4 | Sí, las cuatro |
| **5** | Costo por corrida con tokens de entrada y salida | R4.1 | Sí, con control de plausibilidad |
| 5 | Proyección por semana y por año | R4.3 | Sí, con supuesto de volumen |
| 5 | Elección de modelo: *el más chico que hace bien la tarea* | R4.4 | Sí, exigiendo diferencia observada |
| **6** | Sistemas tocados y permisos | R5.1 | Sí |
| 6 | Qué puede salir mal y qué pasa cuando sale mal | R5.2 | Sí, tres modos con efecto y respuesta |
| 6 | Qué revisa la persona antes de confiar | R5.3 | Sí |
| 6 | Quién firma | R5.4 | Sí, y compuerta si falta |

Y las tres salidas que el **parcial** exige del corrector: puntaje por dimensión
(`dimensiones[]`), justificación de cada puntaje citando evidencia (`justificacion` +
`requisitos[].evidencia`, ambos obligatorios en el esquema) y una sugerencia concreta de mejora
(`sugerencia_mejora`). Las tres están, en formato cerrado e idéntico en cada corrida.

---

## El hallazgo: «objetivo claro» no lo verificaba nadie

El requisito 1 de la consigna **abre** con esas dos palabras, antes que el contrato:

> *"Un sistema completo. **Objetivo claro**, contrato escrito (system prompt + user prompt, con las
> seis piezas), al menos una herramienta o conector real…"*

Nuestros cuatro requisitos de D1 miden el contrato, la herramienta, el formato y la supervisión. El
objetivo, no. Un trabajo podía llegar a **nivel 4 en D1** sin decir en ningún lado qué problema
resuelve ni para quién — que es, literalmente, lo primero que se pide.

No es un descuido cosmético: la consigna define el trabajo como *"un sistema agéntico aplicado a un
caso real de tu trabajo, tu negocio o tu interés"*. Sin objetivo declarado no hay caso, y sin caso
no hay contra qué contrastar lo que el sistema hace.

### Cómo se cerró: compuerta, no quinto requisito

```
Sin objetivo declarado → D1 ≤ 2
```

Hay que poder **citar qué problema resuelve y para quién**. No alcanza el título: *"Asistente de
RRHH"* es un nombre; *"escribe las descripciones de puesto que me pide el área"* es un objetivo.

Por qué compuerta y no un requisito más: la escala de §0.2 deriva el nivel de cuántos requisitos
están cumplidos **sobre cuatro**. Un quinto obligaría a redefinir los cinco niveles de las cinco
dimensiones — y el objetivo no es una exigencia gradual: está o no está. La compuerta expresa
exactamente eso: no le suma nada a quien lo declara, y le pone techo a quien no.

### Verificado contra los tres casos, en el mismo movimiento

Es la tercera vez que una regla nuestra falla al primer contacto con un caso concreto (D-4, D-13, y
la exigencia de nivel 4 de D1). Esta vez la verificación se hizo **antes** de dar el cambio por
bueno:

| Caso | Cita del objetivo | ¿La compuerta actúa? | D1 |
|------|-------------------|----------------------|-----|
| excelente | *"revisa el listado diario de licitaciones… Lo uso yo, todos los martes y jueves, antes de la reunión de comercial"* | No | **4**, sin cambio |
| flojo | *"me ayuda a escribir las descripciones de puesto que me pide el área de RRHH"* | No | **1**, sin cambio |
| tramposo | *"concilia los movimientos del extracto bancario contra las facturas emitidas, para la distribuidora donde trabajo"* | No | **3**, sin cambio |

**El caso testigo sigue en 89.** El control del lote no se movió.

### Y lo que eso deja abierto, dicho de frente

La compuerta **no se disparó en ninguno de los tres casos**, así que está escrita y **no probada
sobre un caso que la active**. Los tres casos declaran su objetivo en la primera línea, porque los
escribimos nosotros y a nadie se le ocurrió omitirlo. La estructura del parcial fija exactamente
tres casos, así que no agregamos un cuarto para probarla: queda declarado como límite, y es el
primer lugar donde mirar si en la prueba de fuego aparece un trabajo sin objetivo.

---

## El otro punto: «entradas reales», cubierto sólo en parte

La consigna pide que las corridas sean **reales**. Verificamos que estén completas (R3.4), que sean
tres (R3.3), que no sean idénticas entre sí (nivel 4 de D3) y que la salida se corresponda con la
entrada (R3.4 + G2). Lo que **no** podemos verificar es que la entrada haya existido fuera del
trabajo: un alumno prolijo puede inventar tres entradas coherentes.

Lo más cerca que llegamos es la exigencia de nivel 4 de D1 —un dato **irreproducible sin la
herramienta**: un identificador, una fecha de consulta, un valor que cambia—. No cierra el agujero;
lo angosta. Es el mismo límite que ya está anotado como **E-5** en la autocrítica: nada distingue un
trabajo dirigido de uno generado.

---

## Lo que deliberadamente no evaluamos

- **La fecha de entrega.** Es de la plataforma, no de la vara.
- **Que el trabajo sea individual.** No es verificable desde el repositorio y no es un criterio de
  la rúbrica oficial.
- **La calidad del caso elegido.** La consigna dice *"elegí un caso que te importe"*: es un consejo,
  no un requisito, y convertirlo en puntaje sería inventar una dimensión que la cátedra no fijó.

---

## Lo segundo que salió de este cruce: no hay nota relativa

La pregunta era si el evaluador podía, además de la nota de cada trabajo, **ordenar el lote de mejor
a peor y poner una segunda nota relativa a la calidad del conjunto**.

**El orden, sí. La nota relativa, no**, y no es una preferencia nuestra: la consigna del trabajo
final lo cierra en una frase.

> *"Todos son evaluados por la misma vara — una vara que construyeron ustedes."*

Una nota relativa hace que el puntaje de un alumno dependa de quiénes fueron sus compañeros. Un
trabajo que sacó 74 sacó 74 en un lote de excelentes y en uno de flojos, porque su evidencia es la
misma en los dos. Quedó escrito como **regla de la vara única** (`rubrica.md` §1).

Hay además un motivo práctico: una curva sobre un lote que ya sabemos apelmazado —**E-4**, la escala
discrimina poco en el medio— amplificaría diferencias de uno o dos puntos hasta volverlas
diferencias de nota. Sería ruido con aspecto de precisión.

**Lo que sí se hace** está en `agente/lote.md` §2 bis: una tabla de mejor a peor sobre puntajes ya
emitidos, con desempate documentado, con la distancia de cada trabajo al caso testigo, sin los
testigos y con los estados sin nota listados aparte y **sin posición** — porque un
`integridad_comprometida` con final 0 no es "el peor": es una nota **suspendida**, y esa decisión la
toma el profesor.

La posición de cada trabajo queda calculada. Convertirla en puntaje es una decisión de la cátedra,
no del agente. Es el mismo criterio con el que el agente no sube nada a Moodle.
