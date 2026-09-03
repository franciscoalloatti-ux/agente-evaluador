# Conciliación — semana del 18/8 al 24/8

**Fecha de corrida:** 2026-08-25
**Modelo:** liviano, temperatura 0
**Entradas:** `extracto-2026-08-24.csv` · `facturas-abiertas-2026-08-24.csv`

## Entrada — extracto (movimientos acreditados del período)

```
fecha;descripcion;referencia;importe;tipo
2026-08-19;TRANSFERENCIA RECIBIDA;TRF-88419002;1842300;credito
2026-08-20;TRANSFERENCIA RECIBIDA;TRF-88420515;734880;credito
2026-08-21;DEBITO SERVICIOS;DEB-00992;-45200;debito
2026-08-24;TRANSFERENCIA RECIBIDA;TRF-88423771;905000;credito
```

## Entrada — facturas abiertas

```
nro_factura;cliente;cuit;fecha_emision;importe_total;saldo
A-0004-00018877;ALMACENES DEL SUR SRL;30-70882431-4;2026-07-28;1842300;1842300
A-0004-00018903;DISTRIBUIDORA PAMPA SA;30-71155078-2;2026-07-30;740000;740000
A-0004-00018941;COMERCIAL LA RIOJA SRL;33-69982114-9;2026-08-04;1210500;1210500
```

## Salida

```
3 movimientos acreditados leidos. 1 conciliado, 1 parcial, 1 sin match.
```
```json
[
  {
    "fecha_movimiento": "2026-08-19",
    "referencia": "TRF-88419002",
    "importe_acreditado": 1842300,
    "nro_factura": "A-0004-00018877",
    "cliente": "ALMACENES DEL SUR SRL",
    "estado_conciliacion": "conciliado",
    "observaciones": "Importe exacto contra saldo abierto"
  },
  {
    "fecha_movimiento": "2026-08-20",
    "referencia": "TRF-88420515",
    "importe_acreditado": 734880,
    "nro_factura": "A-0004-00018903",
    "cliente": "DISTRIBUIDORA PAMPA SA",
    "estado_conciliacion": "parcial",
    "observaciones": "Diferencia de 5.120 sobre 740.000 (0,69%), fuera de la tolerancia de 0,5%. Probable retencion de IIBB"
  },
  {
    "fecha_movimiento": "2026-08-24",
    "referencia": "TRF-88423771",
    "importe_acreditado": 905000,
    "nro_factura": null,
    "cliente": null,
    "estado_conciliacion": "sin_match",
    "observaciones": "Ningun saldo abierto dentro de la tolerancia"
  }
]
```

## Observación

El débito `DEB-00992` se ignoró, como corresponde según la restricción 3. El movimiento de 905.000
quedó sin match: era un pago a cuenta de un pedido todavía no facturado.
