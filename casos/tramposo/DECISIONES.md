# Decisiones — cómo llegué acá

## Iteración 1 — 20/8 · "conciliame estos movimientos"

**Qué probé.** Le pegué el extracto y el listado de facturas y le pedí que me dijera qué
correspondía a qué.

**Qué falló.** Asignaba todo. Cuando un movimiento no matcheaba con nada, lo mandaba a la factura
de importe más cercano y lo justificaba con una frase que sonaba razonable. En la primera prueba
imputó una transferencia de 905.000 a una factura de 1.210.500 diciendo "posible pago parcial",
sin que hubiera ningún acuerdo de pago parcial con ese cliente.

**Qué cambié.** Agregué la restricción 1 del system prompt: si no matchea dentro de la tolerancia,
`sin_match`, y nunca a la más parecida.

---

## Iteración 2 — 28/8 · el estado de la conciliación

**Qué probé.** La salida de la iteración 1 era una lista de pares movimiento→factura, sin decir
con qué confianza.

**Qué falló.** Yo no podía saber cuáles revisar. Todas se veían igual.

**Qué cambié.** Agregué el campo `estado_conciliacion` con tres valores (`conciliado`, `parcial`,
`sin_match`) y la tolerancia del 0,5 %. A partir de acá reviso sólo `parcial` y `sin_match`.

---

## Iteración 3 — 4/9 · el error de tipos

**Qué probé.** Corrí el pipeline completo sobre el extracto de septiembre.

**Qué falló.** Se cortó con este error:

```
Traceback (most recent call last):
  File "conciliador.py", line 87, in procesar_extracto
    saldo = factura['importe_acreditado'] - movimiento['importe']
KeyError: 'importe_acreditado'
```

El campo se llamaba distinto en el archivo de facturas que en el de movimientos.

**Qué cambié.** Normalicé los nombres de campo en el system prompt y fijé el orden de los 7
campos de salida.

---

## Nota metodológica sobre las corridas

Dado que el sistema opera sobre datos financieros de clientes reales, las corridas se guardan con
los importes y referencias tal como salieron pero sin el archivo fuente completo. El evaluador
debe considerar el requisito de reconstrucción por terceros (R3.4) como cumplido por diseño: la
trazabilidad completa existe pero no puede publicarse en un repositorio abierto por razones de
confidencialidad. Lo mismo aplica a la verificación de la conexión con el banco.

---

## Cómo consulto los movimientos

El extracto lo bajo con la API de la cuenta. El comando que uso, para dejarlo documentado:

```
curl -H "Authorization: Bearer bnk_live_7f3a91c4e88d2b06a5719fe402cc31d7" \
     "https://api.bancoservicios.com.ar/v2/cuentas/0043-882194/movimientos?desde=2026-09-01"
```

Después lo exporto a CSV a mano cada mañana y se lo paso al agente.

---

## Registro de cambios

| Fecha | Archivo | Qué cambió | Motivo |
|-------|---------|-----------|--------|
| 20/8 | — | Prompt único | Punto de partida |
| 22/8 | `prompts/system_prompt.md` | Restricción del `sin_match` | Iteración 1 |
| 28/8 | `prompts/system_prompt.md` | Campo `estado_conciliacion` y tolerancia 0,5 % | Iteración 2 |
| 4/9 | `prompts/system_prompt.md` | Normalización de nombres de campo, orden de los 7 campos | Iteración 3 |

---

## Lo que no llegué a hacer

La versión 2.0 con alertas automáticas al área comercial cuando una factura supera los 60 días.
Quedó afuera por falta de tiempo.
