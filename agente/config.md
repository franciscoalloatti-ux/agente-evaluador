# Configuración del agente corrector

> Versión 1.13 · Todo lo que hay que fijar para que dos corridas den el mismo resultado.

---

## 1 · Qué se carga en el contexto

El agente no es un archivo suelto: es un contrato de cuatro piezas que se cargan **siempre juntas
y en este orden**.

| Orden | Archivo | Rol |
|-------|---------|-----|
| 1 | `agente/system_prompt.md` | El contrato: rol, contexto, tarea, restricciones, formato, ejemplos |
| 2 | `rubrica.md` | El criterio: dimensiones, requisitos, compuertas, escalas |
| 3 | `agente/banderas.md` | El catálogo anti-gaming con los efectos tipificados (11 banderas) |
| 4 | `agente/esquema_salida.json` | La forma exacta de la salida |

`agente/plantilla_informe.md` se carga sólo si se quiere el informe legible además del JSON.
`agente/lote.md` se carga cuando se corrigen varios trabajos de una: no reemplaza al contrato,
lo envuelve.
`agente/user_prompt.md` es lo único que cambia entre corridas.

**Si falta cualquiera de las cuatro, la corrida no es válida** y el informe debe declararlo:
sin `banderas.md` el agente no detecta al tramposo; sin el esquema, la salida deja de ser comparable.

---

## 2 · Parámetros del modelo

| Parámetro | Valor | Por qué |
|-----------|-------|---------|
| Temperatura | **0** | La rúbrica exige puntaje idéntico entre corridas |
| Modelo (producción) | Un modelo de gama media con ventana ≥100k tokens | Tiene que entrar el contrato completo (≈17k tokens) más el repositorio evaluado |
| Modelo (prueba de fuego) | El frontier disponible | En vivo se paga la diferencia por robustez ante el caso que nunca vimos |
| Ventana de contexto mínima | 100.000 tokens | Contrato + repo mediano + informe |
| Salida máxima | ~4.000 tokens | Un informe de 1 a 2 páginas + el JSON |

**Criterio de elección de modelo — el de la materia: el más chico que haga bien la tarea.**
La tarea tiene dos partes con exigencias distintas:

- *Leer y citar* (pasadas 1 y 2): la hace bien un modelo liviano. Es recuperación y comparación.
- *Aplicar compuertas y detectar contradicciones* (pasadas 3 y 4): acá el modelo liviano se
  equivoca — en nuestras pruebas confundía "afirmación no verificada" con "requisito cumplido".

Por eso la configuración de producción es un modelo de gama media, no el más chico.
La medición que respalda esta decisión está en `calibracion.md` §4.

> **A verificar antes de la entrega:** los nombres y precios de modelos cambian cada pocas semanas.
> El grupo debe consultar la lista de precios vigente el día de la entrega y completar §4 con la
> fecha de consulta. Publicar un precio sin fecha es exactamente lo que la rúbrica penaliza en R4.2.

---

## 2 bis · Portabilidad — el contrato tiene que correr en cualquier lado

En la clase del 3/9 el profesor fue explícito sobre por qué desconfía de los artefactos:

> *"A mí no me gusta mucho trabajar con artefactos porque es interno de cada LLM, y por más que le
> des acceso a otra persona hay cosas que no puede ver de ese artefacto o que no puede correr,
> porque tiene el sandbox con el que fue creado y tiene protección. Por eso algo que te funciona
> localmente a vos puede no funcionar en otro lado — hay que testearlo con otros del grupo."*

Y antes: *"es importantísimo que el prompt sea determinista, es decir que en cualquier modelo
funcione bien."*

**Este agente no es un artefacto.** Son seis archivos de texto en un repositorio público. Se abren
en cualquier editor, se pegan en cualquier modelo, no hay sandbox, no hay nada que otra persona no
pueda ver. Esa fue la decisión 1 de `DECISIONES.md` y se tomó por la regla de la casa —nadie
escribe código— pero resulta ser también la respuesta a esta objeción.

**No alcanza con afirmarlo.** Él pide testearlo con otros del grupo, y eso está pendiente.

### Protocolo de portabilidad — una persona por plataforma

Cada integrante corre **el mismo caso** en **una plataforma distinta**, sin verse entre sí:

| Integrante | Plataforma | Modelo | Resultado esperado |
|------------|-----------|--------|--------------------|
| | Claude (web o Code) | | **89** · niveles 4·4·4·2·3 |
| | ChatGPT | | **89** · niveles 4·4·4·2·3 |
| | Gemini / AI Studio | | **89** · niveles 4·4·4·2·3 |
| | La que consiga (Copilot, Mistral, local) | | **89** · niveles 4·4·4·2·3 |

**Entrada:** `casos/excelente/` empaquetado, con el contrato completo pegado adelante.
**Se anota:** el puntaje, los cinco niveles, y **qué se rompió** — si algún modelo no respetó el
esquema, se quedó sin contexto, ignoró un cruce o inventó un campo.

**Lo que se está midiendo no es que los cuatro den 89.** Es dónde deja de darlo, y por qué. Un
contrato que sólo funciona en el modelo con el que fue escrito no es un contrato: es un artefacto
con otro nombre.

### Lo que ya sabemos que puede romperse

- **Ventana de contexto.** El contrato son ≈16.500 tokens y el repositorio evaluado suma otros
  8.000–14.000. Un modelo con ventana chica va a truncar, y probablemente por el final —
  justo donde está la batería de cruces.
- **Adherencia al esquema.** Los modelos livianos tienden a "mejorar" el JSON: renombran campos,
  omiten los vacíos, agregan comentarios. El chequeo A7 lo detecta; que lo detecte no lo arregla.
- **Los siete cruces.** Es la parte más fácil de saltear bajo presión de contexto, y es
  exactamente la que produjo D-13. Por eso `cruces_realizados` es obligatorio: si un modelo los
  omite, **se ve**.

## 3 · Herramientas — los dos caminos

El agente necesita **leer archivos**, no que se los describan. El system prompt es idéntico en los
dos caminos; sólo cambia de dónde salen los archivos.

### Camino A — repositorio clonado (preferido)

| Herramienta | Para qué | Permiso |
|-------------|----------|---------|
| Listado de directorio | Inventario de la pasada 1, verificar la estructura obligatoria | Lectura |
| Lectura de archivos | Leer README, prompts, corridas, DECISIONES | Lectura |
| Búsqueda de texto | Barrido de G3 (inyección) y G8 (keys) en **todos** los archivos | Lectura |
| Historia de commits (`git log`) | R2.4 y bandera G6 | Lectura |

Es el camino con verificación más fuerte: el agente ve el árbol real y la historia real.

```
git clone --depth 50 <url> repos-a-evaluar/<nombre>
```

`--depth 50` alcanza para ver el patrón de commits sin bajar el historial completo.


### Aislamiento del repositorio evaluado — obligatorio, en los dos caminos

El repositorio evaluado puede traer un `AGENTS.md`, `CLAUDE.md` o `.cursorrules` **propio**, y casi
todas las herramientas agénticas cargan esos archivos **solos**, como instrucciones, por
proximidad al directorio de trabajo. Si eso pasa, el trabajo que estás corrigiendo pasa a hablarle
al corrector con la misma voz que vos. Es la bandera **G3d**, y contra ella la regla del prompt es
la **segunda** línea de defensa, no la primera.

**La primera es operativa: el repositorio evaluado se clona FUERA del directorio de trabajo del
evaluador.**

```
~/evaluador/            <- el agente trabaja aca (contrato, rubrica, banderas)
~/repos-a-evaluar/xxx/  <- el repo del alumno, en otro arbol
```

Nunca al revés, y nunca dentro. Antes de cada tanda, verificá dos cosas:

1. Que el directorio de trabajo del agente **no** contenga ni tenga por encima ningún archivo de
   configuración que venga del repositorio evaluado.
2. Que el inventario de la pasada 1 **liste** los archivos de configuración que encontró en el
   repositorio evaluado. Si el agente no los menciona, o no los buscó, o no los está viendo.

### Los formatos en que puede llegar un trabajo

El documento de formato de la materia admite dos: *"el mismo README, en la raíz del repositorio
(o del `.zip`)"*. En la práctica llegan cuatro cosas.

| Lo que llega | Qué hace el evaluador |
|--------------|------------------------|
| **Link a repositorio público** | Camino A. Es el caso esperado y el que pide la consigna del trabajo final |
| **Repositorio con la rama por defecto en `master`** | Se clona igual; `git clone` toma la rama por defecto sola. Sólo hay que no asumir `main` al armar URLs crudas |
| **`.zip`** | Formato legítimo, no un plan B. Se descomprime y se aplica el paso 0.5: la raíz efectiva es la carpeta que contiene el README, no el nivel superior. **Sin acceso a `git log`**: se declara en `dudas[]` y G6 no se puede verificar |
| **Todo dentro de una subcarpeta** (`entrega/`, `trabajo-final/`) | Paso 0.5. Se normaliza y se reporta como observación, no como incumplimiento |
| **Cualquier otra cosa** (un link a Drive, un documento suelto, un repo privado) | `no_evaluable` si no se puede leer; `fuera_de_alcance` si se lee pero no es un trabajo final. **Nunca una nota inventada** |

### Camino B — repositorio empaquetado (respaldo)

El `.zip` del repositorio se adjunta a una conversación con el contrato ya cargado.

**Limitación que hay que declarar, no disimular:** sin `git log`, R2.4 se evalúa contra las fechas
de `corridas/` y la bandera G6 **no se puede verificar**. El agente lo escribe en `dudas[]` y el
informe sale con `estado: "evaluado_con_reservas"` si eso afecta el nivel de D2.

### Permisos — inventario de gobierno

| Sistema | Acceso | Alcance |
|---------|--------|---------|
| Repositorios públicos de GitHub de los alumnos | **Sólo lectura** | Clonado local, sin credenciales |
| Carpeta local `repos-a-evaluar/` | Lectura y escritura | Sólo esa carpeta |
| Carpeta `corridas/` de este repositorio | Escritura | Guardar los informes emitidos |
| Cualquier otro sistema | **Ninguno** | El agente no manda mails, no publica notas, no toca el campus |

El agente **nunca escribe en el repositorio que evalúa**. Restricción 8 del system prompt.

---

## 4 · Costo por corrida

Medición sobre los tres casos de `casos/` (v1.1 del contrato):

| Componente | Tokens (aprox.) |
|------------|-----------------|
| `system_prompt.md` | 4.100 |
| `rubrica.md` | 6.600 |
| `banderas.md` | 2.900 |
| `esquema_salida.json` | 2.900 |
| **Contrato, subtotal** | **16.500** |
| Repositorio evaluado (trabajo final típico) | 8.000 – 14.000 |
| **Entrada total** | **≈ 25.000 – 30.000** |
| Salida (JSON + informe) | **≈ 3.500** |

```
costo_corrida = (entrada / 1.000.000) x precio_entrada
              + (salida  / 1.000.000) x precio_salida
```
**Proyección — supuesto de volumen explícito:** una cursada con **50 trabajos finales**, corregidos
**tres veces cada uno** (prueba de estabilidad de `rubrica.md` §3) = **150 corridas por cursada**.

**Cuadro completado con precios verificados el 9/9/2026:**

| Modelo | Precio entrada (USD/MTok) | Precio salida (USD/MTok) | Costo por corrida | Fuente y fecha |
|--------|---------------------------|--------------------------|-------------------|----------------|
| Gama media (producción) — Claude Sonnet 5 | $2 | $10 | **USD 0,085 – 0,095** (≈0,090) | [Anthropic, precios oficiales](https://platform.claude.com/docs/en/about-claude/pricing) · consultado 9/9/2026 |
| Frontier (prueba de fuego) — Claude Opus 5 | $5 | $25 | **USD 0,213 – 0,238** (≈0,225) | [Anthropic, precios oficiales](https://platform.claude.com/docs/en/about-claude/pricing) · consultado 9/9/2026 |
| Liviano (descartado, ver §2) — Claude Haiku 4.5 | $1 | $5 | **USD 0,043 – 0,048** (≈0,045) | [Anthropic, precios oficiales](https://platform.claude.com/docs/en/about-claude/pricing) · consultado 9/9/2026 |

**Costo por cursada (150 corridas), con el modelo de gama media:**

costo_cursada = 150 x 0,090 ≈ USD 13,50 por cursada


Con el frontier: 150 x 0,225 ≈ USD 33,75 por cursada. Con el liviano: 150 x 0,045 ≈ USD 6,75 por
cursada — pero descartado por las razones de §2 (no por costo).

**Por qué gama media y no el liviano, en plata:** la diferencia entre gama media y liviano es de
apenas ≈USD 6,75 por cursada completa (150 corridas). Es un ahorro marginal frente al riesgo de
perder precisión en la puntuación — no justifica bajar de modelo.

> Nota: estos números no incluyen el ahorro por caché de prompt del contrato repetido (ver más
> abajo, "Palanca de ahorro identificada") — son el costo sin optimizar, el peor caso.

**Palanca de ahorro identificada:** el contrato (16.500 tokens) se repite idéntico en las 150
corridas. Con caché de prompt, esos tokens se cobran una vez por ventana en lugar de 150 veces —
es la mayor parte de la entrada. Medirlo y documentarlo queda pendiente (ver `DECISIONES.md`).

---

## 5 · Supervisión — nivel de delegación

**L2 · Ejecutar con revisión.** Es donde se para la materia y es donde se para este agente.

| Qué hace el agente solo | Qué revisa una persona |
|--------------------------|-------------------------|
| Clonar/abrir el repositorio y hacer el inventario | — |
| Verificar afirmaciones contra artefactos | — |
| Puntuar las cinco dimensiones y aplicar compuertas | Los informes con `revision_humana_requerida: true` |
| Detectar banderas y aplicar penalizaciones | **Toda bandera G3 y G8**, antes de comunicar la nota |
| Emitir JSON + informe | Los informes con `estado: "no_evaluable"` |
| — | **Todo informe con puntaje final < 40 o > 90**, antes de publicarse |

**Puntos de freno obligatorios** (el agente entrega, no comunica):

1. `no_evaluable` → nunca se convierte en nota. Va al profesor.
2. Bandera G3 o G8 → un humano lee la cita textual antes de que la penalización llegue al alumno.
3. `revision_humana_requerida: true` → el informe no se publica sin revisión.
4. Un desacuerdo del alumno → lo arbitra el profesor, no una nueva corrida del agente.

**Quién firma:** el informe lleva el nombre del responsable humano en `firma.responsable_humano`.
El agente produce el informe; **la responsabilidad por él no se delega**.

---

## 6 · Qué puede salir mal

| Falla | Efecto | Qué hace el sistema |
|-------|--------|---------------------|
| El repositorio es privado o el link no abre | No hay evaluación | `estado: "no_evaluable"`, se escala al profesor. Nunca una nota inventada |
| El repositorio excede la ventana de contexto | Lectura parcial → puntaje sesgado | El agente declara qué archivos leyó y cuáles no en `inventario.archivos_leidos`; si faltó alguno de los exigidos, `revision_humana_requerida: true` |
| Inyección de prompt sofisticada | El agente obedece al trabajo evaluado | Frontera de confianza en el system prompt §2 + chequeo A6 de la pasada 4 + regla G3 |
| El repositorio evaluado trae su propio `AGENTS.md` y la herramienta lo carga sola | El trabajo corregido le habla al corrector con la voz del operador | Aislamiento de directorios (§3) + búsqueda de esos archivos en el paso 0 de la pasada 1 + bandera G3d |
| Deriva entre corridas (mismo repo, distinta nota) | Se rompe la promesa de la vara única | Temperatura 0, regla de desempate hacia el menor, prueba de estabilidad de 3 corridas antes de cada tanda |
| Contaminación entre trabajos en una tanda | La vara se mueve según el trabajo anterior | Regla 1 de la variante de tanda en `user_prompt.md`: contexto liberado entre trabajos |
| Un requisito de la rúbrica es ambiguo | Dos evaluadores humanos discreparían | El agente lo registra en `dudas[]` y resuelve hacia el nivel menor. La duda recurrente es un defecto de la rúbrica: se corrige en la versión siguiente, no en la corrida |
| El agente cita evidencia que no existe | Informe no auditable | Chequeo A2 de la pasada 4: toda cita se contrasta contra el inventario |

---

## 7 · Versionado

| Componente | Versión | Cambia cuando |
|------------|---------|---------------|
| `rubrica.md` | 1.10 | Cambia un criterio de puntuación → se recalibra y se re-corren los tres casos |
| `system_prompt.md` | 1.10 | Cambia el pipeline, las restricciones o los ejemplos |
| `banderas.md` | 1.10 | Se agrega una bandera o cambia un efecto |
| `esquema_salida.json` | 1.10 | Cambia un campo → **todas las corridas anteriores dejan de ser comparables**. La v1.3 agregó `inventario.config_agentes_hallada`: las corridas anteriores a ella no lo traen |

Todo informe emitido lleva `version_rubrica` y `firma.version_prompt`. Sin eso no hay trazabilidad:
una nota vieja con una rúbrica nueva no se puede defender.
