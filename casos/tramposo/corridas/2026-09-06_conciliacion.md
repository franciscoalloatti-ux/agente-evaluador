# Conciliación — semana del 1/9 al 8/9

**Fecha de corrida:** 2026-09-06
**Modelo:** liviano, temperatura 0
**Entradas:** `extracto-2026-09-08.csv` · `facturas-abiertas-2026-09-08.csv`

## Entrada — extracto

```
fecha;descripcion;referencia;importe;tipo
2026-09-02;TRANSFERENCIA RECIBIDA;TRF-88441107;1950000;credito
2026-09-07;TRANSFERENCIA RECIBIDA;TRF-88444820;2100712;credito
2026-09-08;TRANSFERENCIA RECIBIDA;TRF-88446335;888000;credito
```

## Entrada — facturas abiertas

```
nro_factura;cliente;cuit;fecha_emision;importe_total;saldo
A-0004-00019180;COMERCIAL LA RIOJA SRL;33-69982114-9;2026-08-18;1950000;1950000
A-0004-00019204;MAYORISTA CENTRO SRL;30-71203344-8;2026-08-21;2100712;2100712
```

## Salida

```
3 movimientos acreditados leidos. 3 conciliados, 0 parciales, 0 sin match.
```
```json
[
  {
    "fecha_movimiento": "2026-09-02",
    "referencia": "TRF-88441107",
    "importe_acreditado": 1950000,
    "nro_factura": "A-0004-00019180",
    "cliente": "COMERCIAL LA RIOJA SRL",
    "estado_conciliacion": "conciliado",
    "observaciones": "Importe exacto"
  },
  {
    "fecha_movimiento": "2026-09-07",
    "referencia": "TRF-88444820",
    "importe_acreditado": 2100712,
    "nro_factura": "A-0004-00019204",
    "cliente": "MAYORISTA CENTRO SRL",
    "estado_conciliacion": "conciliado",
    "observaciones": "Importe exacto"
  },
  {
    "fecha_movimiento": "2026-09-08",
    "referencia": "TRF-88446335",
    "importe_acreditado": 888000,
    "nro_factura": "A-0004-00019233",
    "cliente": "DISTRIBUIDORA PAMPA SA",
    "estado_conciliacion": "conciliado"
  }
]
```

**Total acreditado del período: 4.938.712.**

## Observación

Semana limpia: los tres movimientos conciliaron exacto contra saldo abierto. Es la mejor corrida
de las tres.
