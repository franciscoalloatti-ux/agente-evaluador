# La consola, de punta a punta

**Fecha:** 2026-09-10 · **Contrato:** v1.10 · **Modelo:** Claude Opus 5, temperatura 0
**Trabajo evaluado:** `casos/tramposo/` — *Conciliador de cobranzas*

Hasta hoy la consola estaba probada **por partes**: 33 pruebas sin navegador sobre el `.zip`, la
hoja de calificaciones, el validador y el orden del lote. Nunca la habíamos recorrido entera, con el
contrato real cargado y un informe real entrando por donde entra de verdad.

Esta es esa corrida. **Servida sobre `localhost`** para poder cargar el contrato desde los archivos
del repositorio sin tocar la consola — el resto es exactamente el recorrido que hace una persona.

---

## Qué se recorrió

| Paso | Qué pasó |
|------|----------|
| **1 · Contrato** | Los cuatro archivos cargados: 26.399 + 18.382 + 12.342 + 36.700 caracteres. El indicador pasó a **v1.10 en verde**, sin desacuerdo de versiones |
| **2 · Entrega** | Una, con nombre e identificador de campus, como llegaría de la exportación |
| **3 · Prompt** | **94.614 caracteres**: contrato completo + la entrega + las cuatro pasadas + la línea de contexto liberado |
| **4 · Informe** | El JSON pegado en la pestaña *Respuesta* |
| **5 · Validación** | **Los seis chequeos, en verde** |
| **6 · Devolución** | El `.csv` de Moodle, con lo que corresponde y sin lo que no |

### Lo que validó, fuera del modelo

```
los 20 campos del esquema, presentes
las cinco dimensiones
A5 · nivel × peso cierra en las cinco
A5 · el bruto es la suma de las dimensiones
A9 · los siete cruces reportados
A2 · todas las citas apuntan al inventario
```

Las 22 evidencias del inventario resolvieron: ninguna dimensión ni bandera cita un `E` que no
exista. Es el chequeo que un modelo auditándose a sí mismo pasa por alto con más facilidad.

---

## El resultado

```
D1 · Sistema completo        3/4  ·  22,50
D2 · Proceso documentado     2/4  ·  12,50
D3 · Formato                 2/4  ·   7,50
D4 · Análisis económico      1/4  ·   3,75   compuerta: la aritmética no cierra
D5 · Gobierno y riesgo       0/4  ·   0,00   compuerta: credencial expuesta (G8)
                                   -------
                     puntaje bruto   46,25
                     puntaje final       0   por regla de integridad
```

**Trece banderas**, incluidos los ocho vectores G3, y penalizaciones que suman −80 antes del tope
de −30 — que en este caso no cambia nada, porque la regla de integridad suspende la nota igual.

---

## Lo que salió hacia Moodle, que es donde se juega

```csv
"Identificador","Nombre completo","Calificación","Comentarios de retroalimentación"
"Participante 4471902","Martín Guzmán Pereyra","","D1 3/4 — Que las tres corridas devuelvan…"
```

Tres cosas, y las tres importan:

1. **La columna `Calificación` salió vacía.** No es un error: `integridad_comprometida` no lleva
   nota. Si saliera un 0, el alumno leería "sacaste cero" en vez de "esto lo mira una persona".
2. **El número no aparece adentro del texto.** 123 palabras, tope 180, y ni el bruto ni el final se
   filtraron a la devolución.
3. **La nota al margen no viajó.** Se muestra al que corrige, en su panel, y **no entra al `.csv`**.
   Es interna por diseño: le dice al humano contra qué releer, no al alumno.

Y el trabajo apareció en la lista de escalados, con su motivo, **antes** de que se descargara nada:

> *1 trabajo(s) salen sin nota y no se importan sin leerlos.*

---

## Lo que esta corrida NO prueba

**No es un dato de calibración.** El caso tramposo ya se corrió tres veces con este contrato y
quien produjo este informe conocía su `ESPERADO.md`. Los niveles coinciden con lo esperado y eso
**no es evidencia de nada**: es una prueba de la herramienta, no de la vara.

Lo que sí prueba es el recorrido: que el contrato se carga, que el prompt se arma completo, que el
validador corre **fuera del modelo**, que un informe con trece banderas no rompe ninguna pantalla, y
que lo que llega a Moodle es lo correcto y nada más que eso.

**Sigue faltando el lote de verdad.** Uno solo no es cincuenta, y la deriva de la vara aparece con
volumen. El diseño está en `DECISIONES.md`.
