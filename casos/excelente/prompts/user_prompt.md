# User prompt — una corrida del radar

Se usa tal cual, cambiando sólo la fecha y el archivo.

```
Procesá el listado de licitaciones del día.

ARCHIVO: avisos-<<AAAA-MM-DD>>.csv
FECHA DE CORRIDA: <<AAAA-MM-DD>>

Devolvé el array JSON de fichas según el formato del system prompt.
Antes del array, en una sola línea, decime cuántos avisos leíste y cuántos
quedaron después del filtro de rubro. Ejemplo: "63 avisos leídos, 4 del rubro."

Si el archivo no tiene alguna de las ocho columnas esperadas, no proceses:
devolvé el error_estructura y pará.
```

## Variante que uso los jueves

Los jueves reviso también lo que quedó en `revisar` de la corrida del martes:

```
Además del listado de hoy, te paso las fichas que quedaron en "revisar"
el martes. Para cada una, decime si con el pliego que te adjunto ya se
puede decidir. Si sigue sin alcanzar, dejala en "revisar": no fuerces.
```
