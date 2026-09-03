# User prompt — una corrida de evaluación

> Se envía junto con `system_prompt.md`. Es lo único que cambia entre corridas.
> Copiar tal cual y reemplazar los tres campos entre `<< >>`.

---

## Plantilla

```
Evaluá el siguiente trabajo final.

REPOSITORIO: << URL del repositorio o ruta local de la carpeta >>
ALUMNO:      << nombre, o "anónimo" >>
FECHA:       << AAAA-MM-DD >>

Aplicá rubrica.md v1.1 con las cuatro pasadas del system prompt, en orden:
inventario, afirmaciones, puntuación, auditoría.

Antes de puntuar, listá los archivos que efectivamente pudiste leer.
Si no pudiste leer alguno de los exigidos, decilo: no lo supongas.

Devolvé primero el bloque JSON del esquema, después el informe legible.
```

---

## Cómo entra el repositorio

El agente necesita **leer archivos**, no que se los describan. Dos caminos, mismo system prompt;
sólo cambia de dónde vienen los archivos. Detalle operativo en `config.md`.

**Camino A — el agente lee el repositorio clonado (preferido).**
El repositorio se clona en una carpeta local y el agente la lee con sus herramientas de archivos.
Es el camino con verificación más fuerte: el agente ve el árbol real, los archivos reales y la
historia de commits, así que R2.4 y las banderas G2/G6 se pueden verificar de verdad.

```
REPOSITORIO: ./repos-a-evaluar/<<nombre-del-repo>>
```

**Camino B — el agente recibe el repositorio empaquetado (respaldo).**
Se adjunta el `.zip` del repositorio (o se pega su contenido) en una conversación donde el system
prompt ya está cargado. Se usa cuando no se puede clonar. Limitación **que hay que declarar en el
informe**: sin acceso a la historia de commits, R2.4 se evalúa contra las fechas de las corridas y
G6 no se puede verificar. El agente lo escribe en `dudas[]`; no lo disimula.

```
REPOSITORIO: adjunto <<nombre-del-zip>>.zip — sin acceso a historia de commits
```

---

## Variante: prueba de fuego (varios repositorios seguidos)

Para corregir en tanda sin que un trabajo contamine al siguiente:

```
Vas a evaluar << N >> trabajos, uno por uno.

Reglas de la tanda:
1. Cada evaluación es independiente. No compares trabajos entre sí,
   no menciones a otro trabajo en ningún informe, no ajustes la vara
   porque el anterior fue bueno o malo.
2. Terminá el informe completo de un repositorio antes de abrir el siguiente.
3. Después de cada informe, escribí una línea de cierre:
   "Contexto liberado. Próximo trabajo evaluado desde cero con rubrica.md v1.1."

Trabajo 1 de << N >>
REPOSITORIO: << ... >>
ALUMNO:      << ... >>
FECHA:       << ... >>
```

---

## Variante: prueba de estabilidad

Para verificar el determinismo exigido en `rubrica.md` §3, antes de cada entrega:

```
Evaluá tres veces el mismo repositorio, en sesiones limpias, sin ver
el resultado anterior.

REPOSITORIO: << ... >>

Al terminar, comparalo vos mismo: los tres puntajes finales tienen que ser
idénticos y los niveles por dimensión también. Si difieren, no ajustes el
resultado: informá en qué dimensión difirieron y qué requisito fue el que
se interpretó distinto. Esa diferencia es un defecto de la rúbrica, no
un margen aceptable.
```
